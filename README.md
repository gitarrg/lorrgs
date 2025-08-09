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

## Development

```bash

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
```



## Random Info

- `WCL_AUTH_TOKEN` in `.env` and lambda functions requires updating once per year.

### Show logs

```
aws logs tail /aws/lambda/lorrgs-api --follow --since 10m
```
