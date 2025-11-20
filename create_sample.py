import pandas as pd
import os
import json

total_sample_size = 20_000
final_sample = pd.DataFrame()
random_state = 42

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

            temporary_df = pd.json_normalize(loaded_rows)
            print(f"temporary_df.shape: {temporary_df.shape}")
            
            current_sample_size =  total_sample_size / 597_967 * temporary_df.shape[0]
            current_sample = temporary_df.sample(n=int(current_sample_size), random_state=random_state)
            final_sample = pd.concat([final_sample, current_sample], ignore_index=True)

print(f"final_sample.shape: {final_sample.shape}")
final_sample.to_csv(f'data/samples/sample_{total_sample_size}.csv', index=False)

