"""
buzzle/api/words.py
Word banks for the phrase generation engine.
"""

NOUNS = [
    "cactus", "penguin", "developer", "spreadsheet", "deadline", "WiFi",
    "database", "standup", "pivot", "synergy", "bandwidth", "roadmap",
    "kanban", "agile", "scrum", "backlog", "notebook", "thermostat",
    "centipede", "avocado", "algorithm", "404", "commit", "merge",
    "hotdog", "hamster", "blockchain", "cloud", "stack", "pipeline",
    "rubber duck", "semicolon", "namespace", "daemon", "socket",
    "iterator", "refactor", "dockerfile", "linter", "grep",
    "coffee", "monitor", "keyboard", "cursor", "variable", "function",
    "exception", "timeout", "latency", "throughput", "entropy",
    "csv", "json", "yaml", "regex", "terminal", "session",
    "spreadsheet", "pivot table", "dependency", "abstraction",
    "singleton", "mutex", "thread", "garbage collector", "heap",
    "lobster", "flamingo", "ferret", "echidna", "capybara",
    "sourdough", "kombucha", "oat milk", "spreadsheet", "intern",
]

VERBS = [
    "apologizes", "refactors", "deploys", "compiles", "pivots",
    "disrupts", "leverages", "synergizes", "scales", "iterates",
    "optimizes", "bootstraps", "migrates", "containerizes", "commits",
    "branches", "merges", "rebases", "lints", "formats",
    "debugs", "logs", "monitors", "alerts", "retries",
    "timeouts", "caches", "indexes", "queries", "joins",
    "validates", "serializes", "parses", "renders", "hydrates",
    "memoizes", "delegates", "encapsulates", "abstracts", "inherits",
    "overrides", "implements", "integrates", "automates", "orchestrates",
    "provisions", "configures", "patches", "ships", "rolls back",
]

ADJECTIVES = [
    "disciplined", "caffeinated", "confused", "agile", "distributed",
    "asynchronous", "idempotent", "stateless", "immutable", "resilient",
    "scalable", "observable", "containerized", "decoupled", "abstracted",
    "overengineered", "deprecated", "legacy", "bleeding-edge", "robust",
    "blazing-fast", "cloud-native", "data-driven", "AI-powered", "minimal",
    "opinionated", "verbose", "elegant", "pragmatic", "recursive",
    "lazy", "eager", "strict", "loosely-coupled", "eventually-consistent",
    "self-healing", "fault-tolerant", "horizontally-scalable", "serverless",
    "headless", "passwordless", "frictionless", "seamless", "effortless",
]

PREPOSITIONS = [
    "to", "toward", "against", "beyond", "despite",
    "through", "within", "without", "alongside", "underneath",
]

TEMPLATES = [
    "The {adj} {noun} never {verb} {prep} {noun2}.",
    "{verb.title()} harder than your {noun}'s {noun2}.",
    "A {adj} {noun} still knows its {noun2} encoding.",
    "Never let a {adj} {noun} {verb} your {noun2}.",
    "The {noun} that {verb} {prep} {noun2} is already {adj}.",
    "In a world of {noun2}, be the {adj} {noun}.",
    "Your {noun} will {verb} {prep} {noun2} before the sprint ends.",
    "Stay {adj}. Deploy on Fridays. Become the {noun}.",
]
