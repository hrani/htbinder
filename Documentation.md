![alt text](./Images/HillTau_Logo4_360px.png?raw=true "HillTau logo")
# Documentation for HillTau

HillTau has two major usage modes: as a standalone simulator, and as a
library from which HillTau calls are used by other programs. Both these 
are supported by the same two HillTau files: 

	hillTau.py and hillTauSchema.json


## Standalone HillTau syntax

In the present document we provide some examples of how to use HillTau in
standalone mode.

### Getting the syntax: 

```
python hillTau.py -h

	usage: hillTau.py [-h] [-r RUNTIME] [-s STIMULUS [STIMULUS ...]] [-p PLOTS] model

	This is the hillTau simulator. This program simulates abstract kinetic/neural
	models defined in the HillTau formalism. HillTau is an event-driven JSON form to
	represent dynamics of mass-action chemistry and neuronal activity in a fast,
	reduced form. The hillTau program loads and checks HillTau models, and
	optionally does simple stimulus specification and plotting
	 
	positional arguments:
  	model                 Required: filename of model, in JSON format.
	
	optional arguments:
  	-h, --help            show this help message and exit
  	-r RUNTIME, --runtime RUNTIME
	                      Optional: Run time for model, in seconds. If flag is
	                      not set the model is not run and there is no display
	-dt DT, --dt DT       Optional: Time step for model calculations, in
	                      seconds. If this argument is not set the code
	                      calculates dt to be a round number about 1/100 of
	                      runtime.
	-s STIMULUS [STIMULUS ...], --stimulus STIMULUS [STIMULUS ...]
	                      Optional: Deliver stimulus as follows: --stimulus
	                      molecule conc [start [stop]]. Any number of stimuli
	                      may be given, each indicated by --stimulus. By
	                      default: start = 0, stop = runtime
	 -p PLOTS, --plots PLOTS
	                      Optional: plot just the specified molecule(s). The
	                      names are specified by a comma-separated list.
```


### Running a HillTau model
	
Go into the Examples directory and type:

	python ../PythonCode/hillTau.py HT_MODELS/osc.json -r 5000

![alt text](./Images/osc.png?raw=true "Oscillatory model")

This runs the oscillatory model with runtime 5000 seconds, and plots it.

### Selecting only a subset of plots

	python ../PythonCode/hillTau.py HT_MODELS/osc.json -r 5000 -p output
![alt text](./Images/osc_output.png?raw=true "Display only one plot")

	python ../PythonCode/hillTau.py HT_MODELS/osc.json -r 5000 -p output,nfb
![alt text](./Images/osc_output_nfb.png?raw=true "Display two selected plots")

### Giving a stimulus

	python ../PythonCode/hillTau.py HT_MODELS/exc.json -r 20 -s input 1e-3 5 10
![alt text](./Images/singleStim_exc.png?raw=true "Apply single stimulus")

Here we assign molecule 'input' to value 1 uM at time 5 seconds, and
the stimulus turns off at 10 seconds. This is shown in the blue plot.
Note that the units of the model are the default millimolar, so the
stimulus must also be in the same units.

### Giving multiple stimuli

	python ../PythonCode/hillTau.py HT_MODELS/bcm_bistable.json -r 100 -s Ca 2 10 11 -s Ca 0.3 50 80 -p Ca,synAMPAR,on_CaMKII
![alt text](./Images/doubleStim_synapse.png?raw=true "Apply double stimulus")

This model has a bistable mediated by CaMKII feedback, which is triggered by
a Ca input. There is also a Ca-activated phosphatase CaN which acts to 
inhibit and hence turn off the activity of the CaMKII. Thus the Ca input 
both excites the CaMKII, and via CaN, inhibits it. These two counteracting
processes act at different speeds and concentrations.

Here we give a brief strong Ca stimulus to turn on the bistable, and a long,
low Ca stimulus to turn it off again. The CaMKII in turn activates the
synaptic AMPA receptor (synAMPAR) as a readout of synaptic weight. Note that 
the model units are in uM (micromolar), and so the stimulus units are 
handled also in uM.


## Use of HillTau as a library

HillTau provides a set of application functions (API) for use as a library.
These are available both in the Pybind11/C++ and the Python versions. Other
fields or functions may not be supported.

1. loadHillTau( filename )

	Returns: Dictionary of HillTau model as loaded from JSON.
2. getQuantityScale( jsonDict )

	Argument: the dictionary of the model as loaded from JSON.

	Returns: scale factor to use for all quantity conversions. Reference
	units are mM.
3. scaleDict( jsonDict, qs )

	This function goes through the loaded JSON dictionary and rescales all
	concentration quantities by the provided quantityScale qs.

	Argument 1: the dictionary of the model as loaded from JSON.

	Argument 2: the quantity scale.

	There is no return value.
4. parseModel( jsonDict )

	This function parses the JSON dictionary and converts it to a HillTau
	Model object. The Model object is your handle for running the model.

	Argument: the dictionary of the model as loaded from JSON.

	Returns: HillTau Model object
	
Once you have your model, you can run HillTau simulations.

1. 	model.reinit()

	Reinitializes the simulation time to zero, reinitializes all the
	state variables to their starting values.

2.	model.advance( advanceTime, settle = False )

	This advances the simulation by the specified time. The optional 
	_settle_ flag, when True, tells HillTau that intermediate 
	time-points are not needed and to jump very quickly to the steady-state.

### Frequently used classes

There are a couple of frequently used classes.

**MolInfo**: 

This class contains information about each molecule species. Relevant
fields are name, grp and index.

1.	name<br>
	This is a string and is the name of the molecule
2.	grp<br> 
	This is a string and is the name of the group in which the 
	molecule resides. The group location obeys the following convention:

	- All reaction products are located in the same group as their reaction.
	- All equation outputs are located in the same group as their equation.
	- Barring the above, any molecules initialized as 'Species' reside in 
	  the group in which they are defined.
	- Any molecules defined only as reaction substrates reside in the same
	  group as their reaction.
	- Any molecules defined only as equation terms reside in the same
	  group as their equation.
3.	index<br>
	This is an integer. It looks up the molecule concentration in
	the *model.conc* and *model.concInit* arrays.

**Model**:

The Model class exposes a the following fields and functions.

1.	model.molInfo. This is a dict of MolInfos. It is indexed by the name
	of the molecule. The most common use is of the form
	
	```myIndex = input.molInfo.get( "MyMoleculeName" ).index```

2.	model.conc. This is a numpy array of molecule concentrations, indexed
	as using the molecule index. You can get or set it.

	```
	myConc = model.conc[myIndex]
	model.conc[myIndex] = myConc * 2
	```


3.	model.concInit. This is an array of molecule initial concentrations, 
	indexed by the molecule index as above. At 

	```model.reinit()```

	the model.conc vector is initialized to model.concInit.

4.	model.plotvec. This is a list of time-series values of all the
	molecules in the simulation. Every time-step, the entire model.conc
	array is appended to the plotvec. This is how you would get the 
	vector of
	values for myMolecule:

	```myVec = np.transpose( np.array( model.plotvec ) )[myIndex]```

5.	model.dt: This is the timestep of the simulation. User can set it.

6.	model.currentTime: Current time of simulation. User must not set it.

7. 	model.getConcVec( molIndex )
	This function returns the vector of output concentrations as a 
	function of time, for the specified molecule. It is implemented for
	vastly improved performance in the Pybind11/C++ version, as it
	replaces Python transpose and lookup operations on the entire 
	output matrix.

	Argument (integer): molIndex. This is the index of the molecule in the
	vector of concentrations of all molecules. It may be found from
	*MolInfo::index*

	Returns: Vector of output concentrations of specified molecule, as a
	function of time.

	Example: get concs vector for molecule "foo":

	```concs = model.getConcVec( model.molInfo["foo"].index )```



## HillTau model specification format

HillTau uses a JSON format and this is fully specified by a schema file:

	hillTauSchema.json

HillTau has a conversion program **ht2sbml** into SBML, which generates
models that are topologically accurate. These models can be simulated by 
several ODE simulators that read SBML. The conversion is not perfect because
the assumptions in ODE rate models differ from those in HillTau. Specifically,
ODE solvers don't understand the different *tau* and *tau2* terms in HillTau.
The resultant models can be examined by SBML editors and pathway illustrators.

### Units

HillTau uses seconds for time units.

The **QuantityUnits** property specifies one of ["M", "mM", "uM", "nM", "pM"]
as an optional unit for concentration. The default is mM.<br>
Example:
	
	"QuantityUnits": "uM"


### Constants
The *Constants* object has a list of name:value pairs for constants. These
can replace any of the constants below for species initialization, reaction
parameters, or equation terms. Except in the case of *Eqns*, the units are 
as per the **QuantityUnits** above. In the case of *Eqns* the system 
cannot infer what units the user intended, so it uses the values as is.
Recommended way around this is a) to minimize use of equations, and b) if a 
term represents something like a basal concentration, define it in the 
Species list. This gives it clear units of concentration, and then the 
*Constants* scaling will work. <br>
Example:

	"Constants": { "CaBaseline": 0.08, "KA": 1.5, "tau": 0.1 }

### Groups

HillTau organizes all reaction sets into groups. There can be as many groups
as the reaction system requires. This is purely an organizational feature and
has no computational implications, though for systems of any complexity it 
is essential to group reactions in order to keep track and to map properly to
known signaling pathways.

In each group there can be further JSON objects, namely

-	Species

	This is a list of name:value pairs, to specify species name and its 
	initial concentration. Example:
	
		"Species": { "Ca": 0.08, "CaM": 10.0 }

-	Reacs

	This defines reaction steps in the model. In brief, it consists of a
	substrate list followed by a parameter list. The output molecule of 
	the reaction is defined automatically when a reaction is defined, and
	it takes the same name as the reaction itself. This output molecule can
	be used as a substrate in any other reaction.<br>
	There are several optional parameters for each reaction. Example:

			"aTRKb": {
				"subs": [ "TRKb", "aS6K", "BDNF" ],
				"KA": 7.7e-05, "tau": 70 "tau2": 1000,
				"Kmod": 0.5, "Amod": 10e-06, "Nmod": 2,
				"gain": 0.82, "baseline": 5e-06
			}
	
	Each *Reac* is an object with:
	-	Name<br>
		The Reaction name automatically becomes the name of the product
		of the reaction. This product is like any other molecule and can
		be used as a substrate in other reactions or equations.
	-	subs[sub1, sub2...]<br>
		Required list of substrates (array of names). The first 
		substrate is the *reagent*, **R**. The last substrate is 
		the *ligand*, **L**. *L* can be repeated any number of times 
		to denote the order **N** of the reaction:
		
			OutputSteadyState = (R * L^N)/(KA^N + L^N)

		There is an optional 
		middle molecule, the *modifier*. This is based on the analysis
		by Hofmeyer and Cornish-Bowden 1997. 
		It scales *KA* as follows:
		
			k = KA^n * (1+M/Kmod)^h/(1+Amod*(M/Kmod)^h)

	-	KA<br>
		Association constant for reaction. Required. Float.
	-	tau<br>
		Time course for reaction. Required. Float.
	-	tau2<br>
		Time course for reaction decay. Optional. Defaults to same
		as *tau*. Float.
	-	baseline<br>
		Baseline level of output of reaction. Optional. Defaults to 0.
		Float.
	-	gain<br>
		Multiplier for output of reaction. Optional. Default is 1.
	-	Inhibit<br>
		Flag to indicate that the last substrate is an inhibitor.
		0 or 1. Default is 0.
	-	Kmod<br>
		Optional. Float. Scaling constant for any modifier terms into 
		reaction. Must be defined if there is a modifier, should not
		be defined otherwise. Obeys the equation:
		
			k = KA^n * (1+M/Kmod)^h/(1+Amod*(M/Kmod)^h)

	-	Amod<br>
		Optional. Float. Action term for any modifier terms into 
		reaction. The modifier acts in an inhibitory manner when 
		Amod < 1, as an activator when Amod > 1, and has no effect when
		Amod == 1. Default is 4.
	-	Nmod<br>
		Optional. Float. Power *h* to which the modifier fraction is 
		raised. Default = 1.
-	Eqns

	This rarely-used feature defines functions for evaluation
	in cases where the regular reaction structure does not suffice. The
	evaluation is instantaneous, that is, there is no time-course 
	associated with the output of an *Eqn*. Arguments to an equation can be
	molecules, named constants, or numbers.<br>
	Example:

		"eq": "eqBase + eqScale * input + mol + output * 0.3"

	-	Name<br>
		The Equation name automatically becomes the name of a molecule
		whose value is defined by the equation. This can be used as
		a substrate in other reactions or equations.
	-	Equation string<br>
		This is a string expressing an algebraic function to evaluate.
		The function can use any named molecule, standard
		mathematicsl operations and functions, named constants from the
		**Constants** definition, and numbers.

### Group Hierarchy
*Reacs* and *Eqns* are only defined once in each model, so their
location in a group is unambiguous. However, *Species* can be defined
in many possible locations - directly as *Species*, implicitly as 
substrates for *Reacs*, or indirectly as products of *Reacs* or
outputs of *Eqns*. To resolve this. the group location of molecular
*Species* obeys the following convention:

- All reaction products are located in the same group as their Reac.
- All equation outputs are located in the same group as their Eqn.
- Barring the above, any molecules initialized as 'Species' reside in 
  the group in which they are defined.
- Any molecules defined only as reaction substrates reside in the same
  group as their reaction.
- Any molecules defined only as equation terms reside in the same
  group as their equation.

### Species names and namespaces

HillTau creates a molecular species for each of the following:
-	Every species defined with the *Species* keyword
-	Every reaction name
-	Every equation name

HillTau namespace is flat and global, that is, any species defined anywhere
in the system is accessible anywhere in the system.

One can use the *Species* list to initialize the values for molecules 
subsequently defined as a *Reac* or as an *Eqn*. If this initialization
is not done, then initial values the *Reac* and *Eqn* molecules are computed
from the values of the input molecules at initialization time.

### Complete example model

Here is a complete example model, illustrating many of the features above:


	{
		"FileType": "HillTau",
		"Version": "1.0",
		"Author": "Upi Bhalla",
		"Description": "Test case for Equation",
		"Comment": "Conc units are microMolar, time units are seconds",
		"QuantityUnits": "uM",
		"Comment": "Note that HillTau can recognize and rescale units for constants which occur in reactions and species, but not in Eqns.",
		"Constants": { "molBase": 1, "KA": 1, "tau": 1.0, "eqBase":0.0002, "eqScale": 2.0},
		"Groups": {
			"input_g": {
				"Species": {"input": 0.0 }
			},
			"output_g": {
				"Species": {"mol": "molBase" },
				"Reacs": {
					"output": {"subs": ["mol", "input"],
							"KA": "KA", "tau": "tau" }
				},
				"Eqns": {
					 "eq": "eqBase + eqScale * input + mol + output"
				}
			}
		}
	}


## HillTau calculations

HillTau calculations are best explained in the code and in the paper,
mentioned in the [Resources.md](Resources.md) file

Briefly, at each timestep the system calculates the steady-state value for each
reaction using a Hill function, and then uses an exponential decay calculation
to find how far the system would approach it.

The output value of any reaction depends only on its inputs. It is not affected
by any number of downstream reactions that it may plug into. This differs
fundamentally from chemical reactions. It greatly simplifies design of
models and analysis of signal flow, because all information flow is forward.

HillTau now has a Pybind11/C++ version, which is extremely fast. We have
benchmarked it at more than 3 orders of magnitude faster than COPASI or MOOSE
for large equivalent ODE models.
The Pybind11/C++ version is the default library for most users. There is 
also a matching
Python version, preserved for simplicity and to help people understand how it
works. Even in the Python version, the basic HillTau algorithm is highly 
efficient and much faster than ODE simulators for large models.

### HillTau accuracy

For **steady-state calculations**, HillTau has very good accuracy since 
steady-state calculations are the first part of the formulation for every 
reaction. HillTau simply takes very long time-steps
to run the exponential decays down. There are a couple of subtle issues that
arise if the system has interesting dynamical properties such as multistability.

- Multiple stable states: HillTau detects feedback and runs for 10 long steps
	to get these to settle, but it will end up at one of the stable states
	depending on initial conditions.
- Oscillatory systems: These have no stable states and at present HillTau 
	does not report this situation.


For **time-series calculations**, HillTau uses an automatic internal timestep 
assignment to achieve better than 1% accuracy for almost all cases, regardless 
of how long the readout time-steps may be. The current implementation does so
by using short time-stems at the start of every epoch of the simulation.
It takes very short time-steps of 5% of the shortest reaction time-course
_tauMin_ in the system. It uses these short time-steps for at least 
10 _tauMin_, and then reverts to the user-specified timestep. The rationale
is that stimuli are normally delivered by assigning concentrations at the start
of each epoch, and hence the fast transients are present then. After a few
tau the transients settle down.
Based on tests on several models this approach reliably gives <1% accuracy.
This simple approach is not effective when the system is oscillatory,
since the system dynamics are no longer dominated by initial transients.
Here the user should assign model.dt manually to a small-enough value. 

**Definition of accuracy**
Above we use _accuracy_ to mean how closely do the HillTau outputs match those
produced with a very small time-step. Note that HillTau is an approximation
to mass-action chemistry, and uses abstracted models, so the usual caveats 
apply to interpreting numerical accuracy as opposed to accuracy in modeling 
biological systems.

**Useful fields**

The **Model** class of HillTau has some fields useful for managing accuracy:
- _dt_ specifies the plotting timestep, and this is also the default
	timestep for all calculations. Thus higher accuracy may always be
	achieved by reducing _dt_, but this will lead to slower completion of
	simulation runs.
- _internalDt_ specifies the actual timestep used internally.
- _minTau_ specifies the smallest reaction time-course, _tau_, in the entire
	model.


### HillTau outputs

These are accessed from the **Model** class. Use the following options:

- model.plotvec<br>
This is a 2-D array containing output values for all molecules in a HillTau 
model. It is a list of numpy arrays holding all molecule concs at each 
timestep: 

	```model.plotvec[molIndex][timeIndex]```

- model.conc<br>
This is a vector of the current concentrations of each of the
species defined in the model. This is also documented above. One looks it up as:

	```model.conc[molIndex]```


- model.getConcVec( molIndex )<br>
This function returns the vector of output concentrations as a timeseries,
for the specified molecule. It is implemented for
vastly improved performance in the Pybind11/C++ version, as it
replaces Python transpose and lookup operations on the entire 
output matrix.<br>
Example: get concs vector for molecule "foo":

	```concs = model.getConcVec( model.molInfo["foo"].index )```



