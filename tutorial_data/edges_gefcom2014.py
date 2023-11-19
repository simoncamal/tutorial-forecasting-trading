import pandas as pd

metadata = pd.read_csv('metadata_windsites_from_scamal.csv', skiprows=1)

# generate edge features (dlat, dlon)

site_indices = metadata.site_index.values

datas = []
for site_id in site_indices:

    iterable_site = pd.DataFrame({'site_i': [metadata[metadata['site_index'] == site_id].site_name.values[0]
                                             for i in range(len(site_indices))],
        'site_j': metadata['site_name'].values,
        'dlat': metadata[metadata['site_index'] == site_id].lat.values - metadata.lat.values,
        'dlon': metadata[metadata['site_index'] == site_id].lon.values - metadata.lon.values})

    datas.append(iterable_site)

datas_df = pd.concat(datas)

datas_df_wide = datas_df.pivot_table(values=['dlat','dlon'], index='site_i', columns='site_j')

# tuples of column indices
multi_tuples = [('dlat', metadata['site_name'].values[i]) if i % 2 == 0 else ('dlon', metadata['site_name'].values[i]) for i in range(len(metadata['site_name'].values))]

datas_df_wide_reindexed = pd.DataFrame(datas_df_wide, columns=multi_tuples)

datas_df_wide_reindexed = datas_df_wide_reindexed.reindex(datas_df_wide_reindexed.columns.get_level_values(1))

