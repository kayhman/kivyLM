import math


cdef extern from "math.h":
    double fabs(double theta)
    double pow(double a, double x)

cdef extern int autoCorrelationOpt(const char* samples, int size, const double Ethres, const double Athres)
cdef extern char* getKeyName(int key)

def autoCorrelation(const char* samples, int size, const double Ethres, const double Athres):
    key = autoCorrelationOpt(samples, size, Ethres, Athres)
    return key, getKeyName(key)
