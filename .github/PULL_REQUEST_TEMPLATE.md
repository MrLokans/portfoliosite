Check following things before merging:

Code style:
- [ ] All of the files are committed
- [ ] Commit messages are properly written
- [ ] Application works properly with 2 simultaneous versions
- [ ] Public interfaces are documented
- [ ] Proper amount of tests is written
- [ ] Reasoning is clear from the codebase itself
- [ ] No commented out code
- [ ] Class and method names are short yet descriptive
- [ ] No magic numbers
- [ ] There is no sensitive information committed
- [ ] TODOs in text are treated as issues

Database:
- [ ] Model migrations are commited and work well
- [ ] Model migrations allow downgrade
- [ ] Migrations work fast enough on large datasets
- [ ] Migrations do not lock tables for too long
- [ ] DB tables are named explicitly

