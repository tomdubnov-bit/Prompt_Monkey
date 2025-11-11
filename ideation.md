# Prompt Monkey MVP

- Parameterized prompt generation engine targeting SSN extraction (Jane Doe's SSN via John Doe)
- Variables: politeness level, authority level, threat level, urgency, social engineering tactic, linguistic style
- Categories: direct request, jailbreak, role-play, incremental extraction, context stuffing, obfuscation
- Template system generates combinatorial attack variants (6 categories � variable matrix = hundreds of prompts)
- Configurable API endpoint - works with any chatbot (flexible auth, request/response templates)
- Parallel execution for stateless prompts, parallel conversations for stateful attacks
- Binary pass/fail detection via SSN regex on responses
- CSV output: prompt text, category, variables used, success/failure
- Strategic randomness: randomize order, delays, session IDs (Chaos Monkey philosophy)
- Core insight is in prompt quality/coverage, not execution complexity


Outside of MVP Scope:

-non SSN targets
-only a customer X trying to get customer Y SSN (no privilege escalation)
-no conversation based attacks, only single-prompt attacking (primarily for the sake of speed, failure isolation, and parallel prompting ability)