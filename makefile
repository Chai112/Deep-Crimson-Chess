# https://stackoverflow.com/questions/40621451/makefile-automatically-compile-all-c-files-keeping-o-files-in-separate-folde
# written by Chaidhat Chaimongkol 15-05-2020 
# builds C++ for XP11 Windows

CC=g++ # use GCC's C++ compiler

# Directories
BDIR = bin# dir for binaries
SDIR := src# dur for engine source

SRC := $(wildcard $(SDIR).cpp) $(wildcard $(SDIR)/*.cpp) $(wildcard $(SDIR)/*/*.cpp)

#%.cpp:
#	echo $@
#

$(BDIR)/shcr.exe: $(SRC)
	@echo Linking $@
	$(CC) -o $@ $^


