
.PHONY:load save remove

# Save new snapshot of environment 
save: 
	conda env export -n rss-miner -f environment.yml

# Load/update env based on environment file
load: 
	conda env update -n rss-miner -f environment.yml

# Uninstall environment 
remove: 
	conda env remove -n rss-miner -f environment.yml

