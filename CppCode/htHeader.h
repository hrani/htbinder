/************************************************************************
 * This program is part of HILLTAU, a framework for fast compact
 * abstractions of signaling events.
 * Copyright	(C) 2021	Upinder S. Bhalla and NCBS
 * It is made available under the terms of the
 * GNU Public License version 3 or later.
 * See the file COPYING.LIB for the full notice.
************************************************************************/

class Model;

class MolInfo
{
	public:
			MolInfo( const string& name, const string& grp, double concInit );
			string name;
			string grp;
			int order;
			double concInit;
			unsigned int index;
			bool explicitConcInit;
};	

class ReacInfo
{
	public:
			ReacInfo( const string& name, const string& grp, 
			const vector< string >& subs, 
			const map< string, double>& reacObj, 
			const map< string, MolInfo* >& molInfo );
			string name;
			string grp;
			double KA;
			double tau;
			double tau2;
			double Kmod;
			double Amod;
			double Nmod;
			double gain;
			double baseline;
			int inhibit;
			int prdIndex;
			double kh;
			double HillCoeff;
			bool overrideConcInit;
			vector< string > subs;

			double concInf( const vector< double >& conc ) const;
			double eval( Model* model, double dt ) const;
			double getKA() const;
			void setKA( double val );
			int getReacOrder( const Model& model );

	private:
			unsigned int hillIndex;
			unsigned int reagIndex;
			unsigned int modIndex;
			bool oneSub;

};

class EqnInfo
{
	public:
			EqnInfo( const string& name, const string& grp, const string& eqnStr, const vector< string >& eqnSubs, const map< string, MolInfo* >& molInfo, vector< double >& conc );
			string name;
			string grp;
			string eqnStr;
			double eval( vector<double>& conc ) const;
			static vector< unsigned int > findMolTokens(const string& eqn);
			vector< string > subs;
	private:
			// Stuff for parser
			unsigned int molIndex;
			exprtk::symbol_table<double> symbol_table;
			exprtk::expression<double> expression;
};

class Model
{
	public:
			Model();
			map< string, MolInfo* > molInfo;
			map< string, ReacInfo* > reacInfo;
			map< string, EqnInfo* > eqnInfo;
			vector< string > grpInfo;
			map< string, double > namedConsts;
			double currentTime;
			int step;
			double dt;
			double internalDt;	// Timestep to use for internal calculations for time-series. Normally 0.2 * minTau.
			double minTau;	// Smallest time-constant in model.
			vector< double > conc;
			vector< double > concInit;
			vector< vector< double > > plotvec;
			
			void makeMol( const string & name, const string & grp, double concInit );
			void makeReac( const string & name, const string & grp, const vector< string >& subs, const map< string, double >& reacObj );
			void makeEqn( const string & name, const string & grp, const string& expr, const vector< string >& eqnSubs );
			void addGrp( const string& grpname );
			void setReacSeqDepth( int order );
			void assignReacSeq( const string& name, int seq );
			void advance( double runtime, int settle );
			void innerAdvance( double runtime, double newdt );
			void allocConc();
			void parseEqns();
			void reinit();
			vector< double > getConcVec( int index ) const;
			void modifySched( const vector< string >& saveList, const vector< string >& deleteList );
			int getMolOrder( const string& molName ) const;
			bool updateMolOrder(int maxOrder, const string& molName) const;
	private:
			vector< vector< const ReacInfo* > > sortedReacInfo;
			vector< const EqnInfo* > sortedEqnInfo;
};
