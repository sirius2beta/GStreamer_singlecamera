CXX = g++
CXXFLAGS = `pkg-config --cflags --libs gstreamer-1.0`
LIBS = -lwiringPi -lmosquitto

GCAM: GCAM.cpp
	$(CXX) $^ -o $@ $(CXXFLAGS) $(LIBS)
