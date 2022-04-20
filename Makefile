CXX = g++
CXXFLAGS = `pkg-config --cflags --libs gstreamer-1.0`
LIBS = -lwiringPi -lmosquitto
LIBS2 = -lwiringPi -lmosquitto -lpthread

GCAM: GCAM.cpp
	$(CXX) $^ -o $@ $(CXXFLAGS) $(LIBS)

GCAM2: GCAM2.cpp
	$(CXX) $^ -o $@ $(CXXFLAGS) $(LIBS2)
	
GCAM_V2: GCAM_V2.cpp
	$(CXX) $^ -o $@ $(CXXFLAGS) $(LIBS)
	
GCAM_V3: GCAM_V3.cpp
	$(CXX) $^ -o $@ $(CXXFLAGS) $(LIBS)
