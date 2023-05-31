from music.models import Song, Album

def addSongs(l:list, obj):
    obj.songs.add(*l)
    obj.save()

def removeSongs(l:list, obj):
    obj.songs.remove(*l)
    obj.save()


'''
ex, [id, 'a 2,4,5 r 7,8,9']
a -> add
r -> remove
'''
def stringToList(content):
    return list(map(int, content.split(",")))

def commandOperation(content,user):
    opContent = content[1].split(" ")

    obj = Album.objects.prefetch_related('songs').get(pk=content[0])
    if obj.creator == user:
        for i in range(0,len(opContent),2):
            if opContent[i] == 'a':
                addSongs(stringToList(opContent[i+1]),obj)
            elif opContent[i] == 'r':
                removeSongs(stringToList(opContent[i+1]),obj)

        return "Done"
    else:
        return "Only owner can make changes"