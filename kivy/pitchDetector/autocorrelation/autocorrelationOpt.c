#include "math.h"

double computeCorrelation(const short* samples, const int size, const int offset)
{
    double dist = 0.;
    int idx = 0;

    for(idx = 0 ; idx < size ; idx++)
        dist += samples[idx] * samples[(idx+offset)%size];
    return dist;


}

double keyFreq(int key)
{
    return pow(2, (key-49.0) / 12.0) * 440.0;
}

char* getKeyName(const int key)
{
    char* keyString[] = {"Not found", "A0", "A0#", "B0", 
	    		 "C1", "C1#", "D1", "D1#", "E1", "F1", "F1#", "G1", "G1#", "A1", "A1#", "B1",
	    		 "C2", "C2#", "D2", "D2#", "E2", "F2", "F2#", "G2", "G2#", "A2", "A2#", "B2",
	    		 "C3", "C3#", "D3", "D3#", "E3", "F3", "F3#", "G3", "G3#", "A3", "A3#", "B3",
	    		 "C4", "C4#", "D4", "D4#", "E4", "F4", "F4#", "G4", "G4#", "A4", "A4#", "B4",
	    		 "C5", "C5#", "D5", "D5#", "E5", "F5", "F5#", "G5", "G5#", "A5", "A5#", "B5",
	    		 "C6", "C6#", "D6", "D6#", "E6", "F6", "F6#", "G6", "G6#", "A6", "A6#", "B6",
	    		 "C7", "C7#", "D7", "D7#", "E7", "F7", "F7#", "G7", "G7#", "A7", "A7#", "B7",
			 "C8"
    };
    return keyString[key];
}

int autoCorrelationOpt(const char* samples, const int size, const double Athres)
{
    short int* ptr = (short int*)samples;
    double dist = 0.;
    double freq = 0.;
    double maxDist = 0.;
    int offset = 0;
    int note = 0;
    freq = keyFreq(note);
    int key = 0;
    
    const double ct0 = computeCorrelation(ptr, size, 0);

    offset = round(44100.0 / freq);
    dist = computeCorrelation(ptr, size, offset) / ct0;
    maxDist = Athres;
    for(key = 27 ;  key <= 52 ; key++)
    {
        freq = keyFreq(key);
        offset = round(44100.0 / freq);
        dist = computeCorrelation(ptr, size, offset) / ct0;
        if( dist > maxDist)
	{
            maxDist = dist;
            note = key;
	}
    }
    return note;
}
