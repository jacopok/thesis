ylims = (-3, 1)
axs[1].set_ylim(ylims[0]*np.pi, ylims[1]*np.pi)
ticks = np.pi*np.arange(ylims[0], ylims[1]+1)
axs[1].set_yticks(ticks)

labels=[]
for tick in ticks:
    if np.isclose(tick, 0):
        labels.append('$0$')
    elif np.isclose(tick, np.pi):
        labels.append('$\pi$')
    elif np.isclose(tick, -np.pi):
        labels.append('$-\pi$')
    else:
        labels.append(f'${int(tick/np.pi)}\pi$')

axs[1].set_yticklabels(labels)
