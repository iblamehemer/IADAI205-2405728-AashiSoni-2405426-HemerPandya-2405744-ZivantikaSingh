# Large Dataset Note

The file `marketing_campaign_dataset.csv` (26MB, 200,000 rows) exceeds GitHub's 25MB single-file limit.

## Options for the panel:
1. **Download directly** from the Google Drive link in the project brief
2. **Git LFS**: `git lfs track "*.csv"` then push
3. The file IS included in the Streamlit Cloud deployment via the app's built-in datasets

## Dataset Stats:
- Rows: 200,000 campaign records
- Columns: 16 features (Campaign_Type, Channel_Used, ROI, CTR, Engagement_Score, etc.)
- Used for: Ridge regression campaign prediction models
