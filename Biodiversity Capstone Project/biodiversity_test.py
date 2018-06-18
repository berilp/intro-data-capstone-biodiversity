import codecademylib
from matplotlib import pyplot as plt
import pandas as pd

species = pd.read_csv('species_info.csv')

print(species.head())

species_count = species.scientific_name.nunique()
print(species_count)

species_type = species.category.unique()
print(species_type)

conservation_statuses = species.conservation_status.unique()

conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()
print(conservation_counts)

species.fillna('No Intervention', inplace = True)

#conservation counts
conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()

print(conservation_counts_fixed)


protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')

#create graph 1 
plt.figure(figsize=(10,4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)), protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()



#Are certain types of species more likely to be endangered?
species['is_protected'] = species.conservation_status != 'No Intervention'

category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()

#examine
print(category_counts.head())

#pivot
category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()
print(category_pivot)

#rename columns
category_pivot.columns = ['category', 'not_protected', 'protected']

#add new column
category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected)

print(category_pivot)


#contingency table is mammals v. birds 
contingency = [[30, 146], [75,413]]

from scipy.stats import chi2_contingency

ttest, pval, d, ex= chi2_contingency(contingency)
#mammal and bird p-value = 0.6875, therefore not significant
print(pval)

#contingency table is reptile v. mammal
rm_contingency = [[5,73],[30, 146]]

ttest, pval_reptile_mammal, d, ex = chi2_contingency(rm_contingency)
print(pval_reptile_mammal)
#reptile to mammal chi2 test is significant, p-vale = 0.0383

