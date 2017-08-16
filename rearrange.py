import wave
import struct
import numpy as np
from math import log2, pow
from collections import defaultdict


A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

class intervalObj:
    def __init__(self, start, end, halfSteps):
        self.start = start
        self.end = end
        self.halfSteps = halfSteps
 
def pitch(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)

def halfSteps(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return h

if __name__ == '__main__':
    timeline = []
    data_size = 100000
    fname = "MGMT - Kids.wav"
    samplerate = 10000.0
    wav_file = wave.open(fname, 'r')
    data = wav_file.readframes(data_size)
    wav_file.close()
    data = struct.unpack('{n}h'.format(n=data_size), data)
    data = np.array(data)

    #w = np.fft.fft(data)
    print(len(data))
    
    for i in range(0, len(data)-1000, 1000):
        w = np.fft.fft(data[i:i+10000])
        
        
        freqs = np.fft.fftfreq(len(w))
        #print(freqs)
        #print(freqs.min(), freqs.max())
        # (-0.5, 0.499975)

        # Find the peak in the coefficients
        idx = np.argmax(np.abs(w))
        freq = freqs[idx]
        #print(freq)
        freq_in_hertz = abs(freq * samplerate)
        halfStepsResult = halfSteps(freq_in_hertz)
        #print(halfStepsResult)
        interval = intervalObj(((i)/10000), ((i+1000)/10000), halfSteps(freq_in_hertz))
        prev = timeline[-1:]
        #print(prev)
        if len(timeline)>0 and prev[0].halfSteps == halfStepsResult:
            timeline[-1].end = ((i+1000)/10000)
        else:
            timeline.append(interval)
        print(str((i)/10000)+"->"+str((i+1000)/10000)+" seconds: "+ str(freq_in_hertz) +"hz-"+str(pitch(freq_in_hertz)))
        # 439.8975
    
    sortedTimeline = defaultdict(list)
    #print(sortedTimeline)
    
    for i in timeline:
        print(str(i.start)+"-"+str(i.end)+" at "+str(i.halfSteps))
        sortedTimeline[i.halfSteps].append(i)
        
        
    print("----------")
    for h in sortedTimeline:
        for i in sortedTimeline[h]:
            print(str(i.start)+"-"+str(i.end)+" at "+str(i.halfSteps))
    print("---")
        
    rearrangedTimeline = []
    print("---------- this part should be for a new song")    
    for i in timeline:
        desiredTime = i.end - i.start
        acquiredTime = 0
        check = True
        counter = 0
        while(check):
            print(sortedTimeline[i.halfSteps][counter].halfSteps)
            currentClipTime = sortedTimeline[i.halfSteps][counter].end-sortedTimeline[i.halfSteps][counter].start
            print(currentClipTime)
            if(acquiredTime+currentClipTime>desiredTime):
                newClipToAdd = sortedTimeline[i.halfSteps][counter]
                print(str(newClipToAdd.start)+"-"+str(newClipToAdd.end)+" at "+str(newClipToAdd.halfSteps) )
                print(desiredTime)
                print(acquiredTime)
                number = newClipToAdd.start
                newClipToAdd.end = (number + (desiredTime - acquiredTime))
                rearrangedTimeline.append(newClipToAdd)
                print(str(newClipToAdd.start)+"-"+str(newClipToAdd.end)+" at "+str(newClipToAdd.halfSteps) )
                check = False
            else:
                rearrangedTimeline.append(sortedTimeline[i.halfSteps][counter])
                acquiredTime+=currentClipTime
            
            if(len(sortedTimeline[i.halfSteps])==(counter+1)):
                counter = 0
            else:
                counter += 1
            print("counter:"+str(counter))
        
        print('---')
        print("----------")
    for i in rearrangedTimeline:
        print(str(i.start)+"-"+str(i.end)+" at "+str(i.halfSteps))
        print("---")