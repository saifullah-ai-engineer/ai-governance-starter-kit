# Contributing

Thanks for helping improve this starter kit. It is meant for small teams, so keep changes small, clear, and practical.

## How to propose a change

1. Open an issue first if the change is large or changes how a template works. A short description of the problem and the proposed fix is enough.
2. Fork the repository and create a branch with a short, descriptive name.
3. Make your change, then open a pull request. Explain what changed and why, in plain language.
4. If your change affects a template, update the matching example file too, so examples stay in step with the templates.

## Keep it vendor neutral

This kit works with any provider. Do not add content that only works with one vendor, one product, or one paid service. Use generic names in examples, and keep fictional example data clearly fictional.

## Writing style

- Write in plain, direct language.
- Never use an em dash in any file. Use a comma, a period, or a hyphen instead.
- Keep templates short enough for a small team to actually use.

## Tests

- Run the checks before you open a pull request. Every CSV must parse with the Python csv module, every example row must have all columns filled, and every risk score must equal likelihood times impact.
- If you add a new template, add a check for it in the same style as the existing ones.
- Do not merge a change while a test is failing.

## What we will not accept

- Real company data, real customer data, or real credentials in examples.
- Text copied from books, vendor documentation, or other published work. All content here must be original.
