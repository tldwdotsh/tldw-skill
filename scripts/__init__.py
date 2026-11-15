"""Offline skill validation and packaging.

``scripts.validate`` checks the skill files against the hashes recorded in
``skill.json``; ``scripts.build`` writes a deterministic ZIP and release
manifest to ``dist/``. Neither needs credentials or network access.
"""
