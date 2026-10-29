# Deploy

## One time

bootstrap CDK

```sh
scripts/deploy bootstrap aws://{AWS_ACCOUNT}/eu-west-1
```

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
