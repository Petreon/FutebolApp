from loadplayerdata import LoadPlayerData
from player import Player
from field import Field
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from moviepy.editor import VideoFileClip
import os
os.environ['PATH'] += os.pathsep + 'C:\\Users\\Paulo Vitor\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-7.1-full_build\\bin'

player1 = Player()

LoadPlayerData.LoadPlayerCSV(player1,"2023-07-15-M-Juliao-Entire-Session---Live.csv")

field = Field()

field.AppendCorner(-22.890467, -43.228752)
field.AppendCorner(-22.891441, -43.228544)
field.AppendCorner(-22.890335, -43.228034)
field.AppendCorner(-22.890478, -43.228713)

field.CalculateMinMaxCornersLatLong()
field.GetFieldSpecsInMeters()

field.AppendPlayer(player1)

fig, ax = plt.subplots(figsize=(12.7, 7.2)) #1200, 720

# Draw the soccer field
field.draw_soccer_field(ax)

#x1,x2 = field.LatLongToPixelCorners(player1.data[4000].latitude, player1.data[4000].longitude)

## draw a point in it
player1field = field.CreatePlayerField(ax)
#field.UpdatePlayerPosition(player1field,x1,x2)

iterations = 0
const_it = 3
totalIterations = int(len(player1.data))

def initanime():
    return player1field,

def animation(frames:int):
    global iterations
    x1,x2 = field.LatLongToPixelCorners(player1.data[iterations].latitude, player1.data[iterations].longitude)
    field.UpdatePlayerPosition(player1field,x1,x2)

    iterations += const_it
    return player1field,


ani = FuncAnimation(fig,animation, init_func=initanime ,frames=int(totalIterations/const_it)-1,interval=1,blit=True)



# Plotting player positions
#ax.scatter(df.iloc[:,2],df.iloc[:,3], color = colors[0])
plt.xlim(0, 3840)
plt.ylim(0, 2160)
plt.gca().invert_yaxis()  # Invert y-axis to match image coordinates
plt.title('Team 1 player 1 Trajectory', fontsize = 24)
ax.axis('off')

gif_filename = 'player_trajectory.gif'
#ani.save(gif_filename, writer='pillow', fps=24)
ani.save("player_trajectory.mp4", writer='ffmpeg', fps=24)

# Step 2: Convert GIF to MP4 using moviepy
#clip = VideoFileClip(gif_filename)
#mp4_filename = 'player_trajectory.mp4'
#clip.write_videofile(mp4_filename, codec='libx264')

plt.close(fig)  # Close the figure if you don't want to display it
#plt.show()

