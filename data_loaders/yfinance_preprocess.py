import pandas as pd


class preprocess():
    def __init__(self, data, selectedCurrrencies, DateInterval, holcv):
        self.data = data
        self.selectedCurrencies = selectedCurrrencies
        self.DateInterval = DateInterval
        self.holcv = holcv

    def cleanDataFrame(self):
        clean_df_list = []
        for tic in self.selectedCurrencies:
            clean_df = pd.DataFrame(index=self.DateInterval,
                                    columns=self.holcv + ['tic'])

            for i, info in enumerate(self.holcv):
                selectedData = self.data[i]
                ticData = selectedData[tic]
                clean_df[info] = ticData
            clean_df['tic'] = tic
            clean_df_list.append(clean_df)
        dataframe = pd.concat(clean_df_list)

        return dataframe
