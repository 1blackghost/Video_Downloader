'''
Module used to work with youtube downloading videos and audios.
'''
from pytube import YouTube

class Y_D:
    '''
    Main class of youtube downloader
    Arguments Expected: url

    '''
    def __init__(self,url):
        self.url=url
        self.yt = YouTube(self.url)
    def get_title(self):
        '''
        Returns the title of the youtube video
        
        returnType:str
        '''
        return self.yt.title
    def check_available(self):
        '''
        This function checks all the res and formats available and return a dictionary of data
        that can be able to work with python,most of the objects cannot be found in stream are
        extracted using split method

        returnType:dictionary
        
        avg resp time:2s-3s

        sample return value:
        {'video': 
            {'"144p"': ['video/webm', 'video', False], 
            '"360p"': ['video/webm', 'video', False], 
            '"720p"': ['video/webm', 'video', False], 
            '"2160p"': ['video/webm', 'video', False], 
            '"1440p"': ['video/webm', 'video', False], 
            '"1080p"': ['video/webm', 'video', False], 
            '"480p"': ['video/webm', 'video', False], 
            '"240p"': ['video/webm', 'video', False]}, 
        'audio': 
            {'48kbps': ['audio/mp4', 'audio'], 
            '128kbps': ['audio/mp4', 'audio'], 
            '50kbps': ['audio/webm', 'audio'], 
            '70kbps': ['audio/webm', 'audio'], 
            '160kbps': ['audio/webm', 'audio']
            }
        }
        '''
        d={}
        #for video dictinary
        d_video={}
        #for audio dictionary
        d_audio={}
        for stream in self.yt.streams:
            data=[]
            type=stream.type
            data.append(stream.mime_type)
            #if the type is video appends into video dict
            if str(type)=="video":
                data.append(type)
                res=str(stream).split(" ")[3].split("=")[1]
                data.append(stream.is_progressive)
                d_video[res]=data
            #otherwise audio dictionary
            elif str(type)=="audio":
                data.append(stream.type)
                d_audio[stream.abr]=data
        #appending to the parent dictionary audio and video dictionary
        d["video"]=d_video
        d["audio"]=d_audio  
        return d
    def download(self,res,data):
        '''
        Downloads youtube video/audio in the passed formats
        
        expected arguments:res|abr:str , data :list(in order generated by check_available)
        returnType:None
        '''
        if data[1]=="video":
            self.yt.streams.filter(res=res,mime_type=data[0],progressive=data[2]).first().download("static")
        
        elif data[1]=="audio":
            self.yt.streams.filter(abr=res,mime_type=data[0]).first().download("static")
