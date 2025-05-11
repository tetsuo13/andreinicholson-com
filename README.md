# andreinicholson.com

This is the personal website https://andreinicholson.com/

Built with [Hugo](https://gohugo.io/).

## Getting started

Run these commands in parallel using multiple terminals:

```
npm run watch-css
```

```
hugo serve
```

There are several GitHub Actions workflows that aid in development:

- [Compress Images](./.github/workflows/calibreapp-image-actions.yml) workflow triggers on pull requests to find and compress any images that may have been added.
- Markdown linter for blog posts. As part of the [CI](./.github/workflows/ci.yml) workflow, a linter will run to ensure some rules are followed when writing posts -- like SEO, for example.

## License

* [MIT License](./LICENSE.md) for code
* [CC-BY-SA 4.0](./ASSET_LICENSE.md) for content
