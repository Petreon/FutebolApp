import pandas as pd
from player import Player
from datapoint import DataPoint

class LoadPlayerData:

    @staticmethod
    def LoadPlayerCSV(player: Player, fileName: str, dataToRead:int = 0) -> None:
        data_player = pd.read_csv(fileName)
        player.name = data_player["Player Display Name"].iat[0]
        totalDataToRead = 0

        if dataToRead == 0:
            totalDataToRead = len(data_player)
        else:
            totalDataToRead = dataToRead

        for i in range(totalDataToRead):
            playerDataobj = DataPoint(
                data_player["Time"].iat[i],
                data_player["Lat"].iat[i],
                data_player["Lon"].iat[i],
                data_player["Speed (m/s)"].iat[i],
                data_player["Heart Rate (bpm)"].iat[i],
                data_player["Instantaneous Acceleration Impulse"].iat[i]
            )

            player.data.append(playerDataobj)
        
