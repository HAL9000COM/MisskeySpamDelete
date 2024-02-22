# Misskey Spam Delete

## What is this?

A simple Python script to delete spam users from Misskey.

## Requirements

- Misskey API key with admin permission.
- Search enabled on Misskey instance.

## How to use

```python

python3 main.py -u https://misskey.example -t AbCdEfGh -k spam -l spam_delete.log

```

### Options

|Options|Description|
|-------|-----------|
| -u, --url| Misskey URL |
| -t, --token| Access Token |
| -k, --keyword| Keyword to search |
| -a, --action| Action (delete or suspend user), Manual choice for each post if not provided |
| -l, --log| Log output to filepath |

## TODO

- [ ] Add more options (search by instance, etc.)
- [ ] Add more actions（delete posts, etc.）
