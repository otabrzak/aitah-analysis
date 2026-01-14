# aitah-analysis
# Data fetching
Since the json dataset is currently too large to keep on GitHub, the `data` folder has to be downloaded from OneDrive and replaced manually.

# Pre-made samples
I have prepared a few clean and processed csv samples so minimal preprocessing is needed. They are in the folder `data/samples`. *Balanced* means the classes were undersampled to be equally distributed (50/50) and the sampled data was cleaned. *Preprocessed* means the data was only been cleaned and the original ratio between classes was left intact.

# Creating a sample
You can create a sample yourself through the script `data_scripts/script_sample_from_yearly.py`. At the start of the script, there are adjustable parameters (*sample size*, *random state* and *balance* - the option to balance the sample).

# Submission attributes
Here are some of the most important attributes in the original JSONs (as per the [PRAW documentation](https://praw.readthedocs.io/en/stable/code_overview/models/submission.html)).
| Attribute | Description |
| :--- | :--- |
| `author` | Provides an instance of `Redditor`. |
| `author_flair_text` | The text content of the author’s flair, or `None` if not flaired. |
| `clicked` | Whether or not the submission has been clicked by the client. |
| `comments` | Provides an instance of `CommentForest`. |
| `created_utc` | Time the submission was created, represented in Unix Time. |
| `distinguished` | Whether or not the submission is distinguished. |
| `edited` | Whether or not the submission has been edited. |
| `id` | ID of the submission. |
| `is_original_content` | Whether or not the submission has been set as original content. |
| `is_self` | Whether or not the submission is a selfpost (text-only). |
| `link_flair_template_id` | The link flair’s ID. |
| `link_flair_text` | The link flair’s text content, or `None` if not flaired. |
| `locked` | Whether or not the submission has been locked. |
| `name` | Fullname of the submission. |
| `num_comments` | The number of comments on the submission. |
| `over_18` | Whether or not the submission has been marked as NSFW. |
| `permalink` | A permalink