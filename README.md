# Oversee
Helps oversee your Ubuntu OS!

Want to install CLion with one command? Or Google Chrome? Or all of your development software? How about a cleaner and easier way to define your .bash_aliases? Or an easier way to perform secure file transfers? This package will help!


## Installation
```
pip install oversee
oversee --help
```

Place an `.oversee.yaml` in your home directory (ex. `~/.oversee.yaml`). See `examples/` for some examples!

## Example Usage
```
# Install a package
oversee install clion

# Export your bash aliases to ~/.bash_aliases
oversee export

# Move a file to your local machine where `test` is a host defined in `.oversee.yaml`
oversee move test:~/file.txt ~/
```

## Roadmap
- [ ] Added jetbrains settings sync support
- [ ] Make environments work
- [ ] Add project management components (make releases)
- [ ] Autocomplete functionality
- [ ] maybe use builtin functionality for file transfer
- [ ] Add list commands using decorator
- [ ] Add jetbrains .gitignore command
