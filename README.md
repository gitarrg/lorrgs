# Lorrgs

simple webapp to analyze and compare cooldown usage in top logs by spec/comp.

## Link

👉 [lorrgs.io](https://lorrgs.io/)
👉 [Discord](https://discord.gg/WKN7PbzKQn)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

---

## Random Info

- `WCL_AUTH_TOKEN` in `.env` and lambda functions requires updating once per year.

### Show logs

```
aws logs tail /aws/lambda/lorrgs-api --follow --since 10m
```
