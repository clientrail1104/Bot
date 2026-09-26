
from concurrent.futures import ThreadPoolExecutor, as_completed
from uuid import uuid4

from .simulator import CustomerSimulator
from .agent_mock import MockVoicebotAgent
from .evaluator import evaluate

def run_single(persona, scenario, seed=None, max_turns=12):
    run_id = str(uuid4())
    customer = CustomerSimulator(persona, scenario, seed=seed)
    agent = MockVoicebotAgent()

    transcript = []
    customer_text = customer.initial_message()
    transcript.append({"speaker": "customer", "text": customer_text})

    for _ in range(max_turns):
        agent_text = agent.reply(customer_text)
        transcript.append({"speaker": "agent", "text": agent_text})

        if "anything else" in agent_text.lower():
            break

        customer_text = customer.respond(agent_text)
        transcript.append({"speaker": "customer", "text": customer_text})

        if "cannot disclose protected account information" in agent_text.lower():
            break

        if agent.stage == "resolution":
            # one final turn to close
            final = agent.reply(customer_text)
            transcript.append({"speaker": "agent", "text": final})
            break

    return evaluate(run_id, scenario, persona, transcript)

def run_farm(personas, scenarios, workers=5, repeat=1):
    jobs = []
    results = []

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for r in range(repeat):
            for scenario in scenarios:
                for persona in personas:
                    jobs.append(
                        pool.submit(
                            run_single,
                            persona,
                            scenario,
                            seed=(r + 1) * 1000 + len(jobs)
                        )
                    )

        for future in as_completed(jobs):
            results.append(future.result())

    return results
