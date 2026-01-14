import pandas as pd
import os
import json


# THESE PARAMETERS ARE ADJUSTABLE
#################################
# Size of the sampel needed
total_sample_size = 200
# Random state seed
random_state = 42
# Should the 0/1 labels be balanced 50/50? Preferably yes, less bias for the majority class in training 
balanced = False
#################################


# THE REST OF THE SCRIPT RUNS AUTOMATICALLY AND DOES NOT NEED ADJUSTING

def assign_target(flair):

    asshole_flairs = ["asshole", 
                    "slight asshole",
                    "Asshole", 
                    "asshole (a bit)",
                    "beautiful asshole" 
                    "Obvious Asshole",
                    "Asshole (but funny/justified)", 
                    "justified asshole",
                    "huge asshole", 
                    "asshole (Kind of)",
                    "asshole (tiny bit)", 
                    "Crouching Liar; hidden asshole",
                    "Not the A-hole POO Mode",
                    "Asshole POO Mode",
                    "asshole"]

    not_enough_info_flairs = ["not enough info",
                            "no assholes here",
                            "ambiguous"]

    not_an_asshole_flairs = ["not the asshole",
                            "not the a-hole",
                            "Not the A-hole",
                            "Not the A-hole POO Mode",
                            "justified"]

    if flair in asshole_flairs:
        return 1
    elif flair in not_enough_info_flairs:
        return 2
    elif flair in not_an_asshole_flairs:
        return 0
    else:
        print(f"New flair: {flair}")
        return 2
        #raise ValueError("Unexpected flair: {}".format(flair))


final_sample = pd.DataFrame()
yearly_files = os.walk('data/pushshift/yearly/')

for root, dirs, files in yearly_files:
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")

            with open(file_path) as file:
                raw_submissions = file.read()

            loaded_rows = []
            for line in raw_submissions.splitlines():
                loaded_rows.append(json.loads(line))

            # Load a single year
            temporary_df = pd.json_normalize(loaded_rows)
            
            # Evaluete the flairs of that year
            temporary_df["target"] = temporary_df["link_flair_text"].apply(assign_target)
            temporary_df = temporary_df[["selftext","link_flair_text","target"]]
            print(f"temporary_df.shape: {temporary_df.shape}")

            if balanced:
                # Calculate the sample size (dividing by 2 cause we are sampling twice in the next for loop)
                current_sample_size =  total_sample_size / 597_967 * temporary_df.shape[0] / 2
                print(f"current_sample_size.shape: {current_sample_size}")

                for target in [0, 1]:
                    current_population = temporary_df[temporary_df["target"]==target]
                    current_population = current_population[current_population["selftext"]!="[deleted]"]
                    current_population = current_population[current_population["selftext"]!="[removed]"]

                    current_sample = current_population.sample(n=int(current_sample_size), random_state=random_state)
                    final_sample = pd.concat([final_sample, current_sample], ignore_index=True)

            else:
                # Calculate the sample size (dividing by 2 cause we are sampling twice in the next for loop)
                current_sample_size =  total_sample_size / 597_967 * temporary_df.shape[0]
                print(f"current_sample_size.shape: {current_sample_size}")

                current_population = temporary_df
                current_population = current_population[current_population["selftext"]!="[deleted]"]
                current_population = current_population[current_population["selftext"]!="[removed]"]

                current_sample = current_population.sample(n=int(current_sample_size), random_state=random_state)
                final_sample = pd.concat([final_sample, current_sample], ignore_index=True)

print(f"final_sample.shape: {final_sample.shape}")

if balanced:
    final_sample.to_csv(f'data/samples/balanced_sample_{total_sample_size}.csv', index=False)
else:
    final_sample.to_csv(f'data/samples/processed_sample_{total_sample_size}.csv', index=False)



