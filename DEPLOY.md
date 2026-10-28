# Deploy

## One time

setup github secrets

```sh
# edit .env
gh secret set --repo gitarrg/lorrgs --env-file .env
```

## Update

```sh
# preview
scripts/deploy diff

```
