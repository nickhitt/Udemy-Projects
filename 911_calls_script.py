import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("911.csv")

print(df.info)
print(df.head)

### Basic Questions

# Top zip codes for 911 calls
zip_counts = df.groupby('zip')['zip'].count()
top_zip = zip_counts.sort_values(ascending=False)
top_zip.head

# Top townships for 911 calls
twp_counts = df.groupby('twp')['twp'].count()
top_twp = twp_counts.sort_values(ascending=False)
top_twp.head

# Unique vals in title
un_title = len(df['title'].unique())

### Creating new features

# Reasons for call
df["reason"] = df['title'].apply(lambda y: y.split(':')[0])
reason_counts = df.groupby('reason')['reason'].count()
top_reason = reason_counts.sort_values(ascending=False)
top_reason.head

# Countplot of reasons for call
ax = sns.countplot(x="reason", data=df)

# Datatype of columns
df.dtypes

# Converting timestamps to date-times
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)

# Mapping integer day of week to days
dmap = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)

# Making count map of day of week
ax = sns.countplot(x="Day of Week", data=df, hue = 'reason')
# Making count map of Month
ax = sns.countplot(x="Month", data=df, hue = 'reason')
## Months missing which is odd

byMonth = df.groupby('Month').count()
byMonth.head()
# Plot of calls by month
fig = plt.figure()
ax = plt.axes()
ax.plot(byMonth['reason']);

# Regression of calls by month
byMonth = byMonth.reset_index()
g = sns.lmplot(x="Month", y="reason", data=byMonth)

# Creating 'date' column
df['date'] = df['timeStamp'].apply(lambda y: y.date())

# All calls
df.groupby('date').count()['twp'].plot()
plt.tight_layout()
# EMS Calls
df[df["reason"] == "EMS"].groupby('date').count()['twp'].plot()
plt.tight_layout()

df[df["reason"] == "Fire"].groupby('date').count()['twp'].plot()
plt.tight_layout()

df[df["reason"] == "Traffic"].groupby('date').count()['twp'].plot()
plt.tight_layout()

### Heatmaps

# Restructuring data for day of week and hour
restructured = df.groupby(["Day of Week", "Hour"]).count()['reason'].unstack()
# Heatmap of df
ax = sns.heatmap(restructured)
# Cluster heatmap
ax = sns.clustermap(restructured)

# Restructuring data for day of week and month
restructured = df.groupby(["Day of Week", "Month"]).count()['reason'].unstack()
# Heatmap of df
ax = sns.heatmap(restructured)
# Cluster heatmap
ax = sns.clustermap(restructured)