/** @file main.cpp Main strating module for running configLego library
 *	Config Lego system
 *
 */
#include "lego.h"
using namespace std;

// global variable to store number of nodes defined so far
extern int num_nodes;

void getDomMap(Domain dom);

int main(void)
{
	Query qr1;

	// initiate Lego system
	InitLego(1000000, 10000);

	cout << "Lego System" << endl;

	Network N;

	AddDomain(DB, "terra/ec2-db.txt", N);
	AddDomain(WEB, "terra/ec2-http.txt", N);
	AddDomain(NET, "terra/net.txt", N);


	Domain doms[] = {WEB, DB, NET};

	AddRouter(R1, "terra/r1.txt", N);

	AddFirewall(SGDB, "terra/sg-db.txt", N);
	AddFirewall(SGWEB, "terra/sg-web.txt", N);
	AddFirewall(EDGE, "terra/edge.txt", N);
	

	N.link(R1, 1, SGWEB, 1);
	N.link(R1, 2, SGDB, 1);
	N.link(R1, 3, EDGE, 1);

	N.link(SGWEB, 2, WEB, ANY_IFACE);
	N.link(SGDB, 2, DB, ANY_IFACE);
	N.link(EDGE, 2, NET, ANY_IFACE);



	// AddDomain(DNet, "config/dneB.txt", N);
	// AddDomain(DDMZ, "config/ddmz.txt", N);
	// AddDomain(DEng, "config/deng.txt", N);
	// AddDomain(DAcc, "config/dacc.txt", N);
	// AddDomain(DMark, "config/dmark.txt", N);

	// //
	// // Temp
	// //
	// Domain doms[] = {DDMZ, DEng, DAcc, DMark};

	// AddRouter(R0, "config/r0.txt", N);
	// AddRouter(R1, "config/r1.txt", N);
	// AddRouter(R2, "config/r2.txt", N);
	// AddRouter(R3, "config/r3.txt", N);

	// AddFirewall(F1, "config/fw1.txt", N);
	// AddFirewall(F2, "config/fw2.txt", N);
	// AddFirewall(F3, "config/fw3.txt", N);
	// AddFirewall(F4, "config/fw4.txt", N);
	// AddFirewall(F5, "config/fw5.txt", N);


	// //N.link(R0, 1, DNet, ANY_IFACE);   //Connecting core router to Domain 1
	// N.link(F1, 1, R0, 2);

	// N.link(R1, 1, F1, 2); 
	// N.link(R1, 2, F2, 1);
	// N.link(R1, 3, F3, 1);
	// N.link(F2, 2, DDMZ, ANY_IFACE);

	// N.link(R2, 1, F3, 2);
	// N.link(R2, 2, DEng, ANY_IFACE);
	// N.link(R2, 3, F4, 1);

	// N.link(R3, 1, F4, 2);
	// N.link(R3, 2, DAcc, ANY_IFACE);
	// N.link(R3, 3, F5, 1);
	// N.link(F5, 2, DMark, ANY_IFACE);


	//
	// Temp: Print the network
	//
	N.print();


	N.buildDeviceBDD();
	N.buildGlobalBDD();

	cout<<"Global BDD Built"<<endl;

	cout << "Main ID : " << WEB.nid() << endl;
	N.getDomMap(&WEB);
	cout<<"--------------------------"<<endl;

	vector<config_node*> fVec;
	vector<config_node*> gVec;

	N.getPathObjects(WEB, DB, fVec, ANY_NODE);
	cout<< WEB.node_name() << " - " << DB.node_name() << " = "<<fVec.size()<<endl;
	for (vector<config_node*>::iterator n=fVec.begin(); n!=fVec.end(); n++)
		cout << (*n)->node_name() << " -> ";
	cout<<endl;
	fVec.clear();

	N.getPathObjects(DB, WEB, fVec, ANY_NODE);
	cout<< DB.node_name() << " - " << WEB.node_name() << " = "<<fVec.size()<<endl;
	for (vector<config_node*>::iterator n=fVec.begin(); n!=fVec.end(); n++)
		cout << (*n)->node_name() << " -> ";
	cout<<endl;
	fVec.clear();


	N.getPathObjects(WEB, NET, fVec, ANY_NODE);
	cout<< WEB.node_name() << " - " << NET.node_name() << " = "<<fVec.size()<<endl;
	for (vector<config_node*>::iterator n=fVec.begin(); n!=fVec.end(); n++)
		cout << (*n)->node_name() << " -> ";
	cout<<endl;
	fVec.clear();

	N.getPathObjects(NET, DB, fVec, ANY_NODE);
	cout<< NET.node_name() << " - " << DB.node_name() << " = "<<fVec.size()<<endl;
	for (vector<config_node*>::iterator n=fVec.begin(); n!=fVec.end(); n++)
		cout << (*n)->node_name() << " -> ";
	cout<<endl;
	fVec.clear();
	
	
	int choice = 5, cnt;
	while (choice != 5)
	{
		/*
		cout<<"===================================================="<<endl;
		cout<<"Please select a choice:"<<endl;
		cout<<"  1. Get Path."<<endl;
		cout<<"  2. Print all paths."<<endl;
		//cout<<"  3. Verify the requirements."<<endl;
		//cout<<"  4. Show all traffic that can reach R3 but blocked by FW1."<<endl;
		cout<<"  5. Exit."<<endl<<endl;

		cout<<"Enter your choice : ";
		cin>>choice;
*/
		

		switch (choice)
		{
			case 1:
				//
				// DDMZ, DEng, DAcc, DMark
				//




				// N.getPathObjects(DDMZ, DNet, fVec, ANY_NODE);
				// cout<< DDMZ.node_name() << " - " << DNet.node_name() << " = "<<fVec.size()<<endl;
				// for (vector<config_node*>::iterator n=fVec.begin(); n!=fVec.end(); n++)
				// 	cout << (*n)->node_name() << " -> ";
				// cout<<endl;

				// N.getPathObjects(DEng, DDMZ, gVec, ANY_NODE);
				// cout<< DEng.node_name() << " - " << DDMZ.node_name() << " = "<<fVec.size()<<endl;
				// for (vector<config_node*>::iterator n=gVec.begin(); n!=gVec.end(); n++)
				// 	cout << (*n)->node_name() << " -> ";
				// cout<<endl;

				// fVec.clear();
				// N.getPathObjects(DDMZ, DAcc, fVec, ANY_NODE);
				// cout<< DDMZ.node_name() << " - " << DAcc.node_name() << " = "<<fVec.size()<<endl;
				// for (vector<config_node*>::iterator n=fVec.begin(); n!=fVec.end(); n++)
				// 	cout << (*n)->node_name() << " -> ";
				// cout<<endl;

				// fVec.clear();
				// N.getPathObjects(DDMZ, DMark, fVec, ANY_NODE);
				// cout<< DDMZ.node_name() << " - " << DMark.node_name() << " = "<<fVec.size()<<endl;
				// for (vector<config_node*>::iterator n=fVec.begin(); n!=fVec.end(); n++)
				// 	cout << (*n)->node_name() << " -> ";
				// cout<<endl;

				break;
			case 2:
				cnt = 3;
				cout << cnt << endl;
				for (int i=0; i<cnt; i++)
					for (int j=0; j<cnt; j++)
					{
						if (i==j)
							continue;

						fVec.clear();

						cout << doms[i].node_name() << " - " << doms[j].node_name() << endl;

						N.getPathObjects(doms[i], doms[j], fVec, ANY_NODE);
						for (vector<config_node*>::iterator n=fVec.begin(); n!=fVec.end(); n++)
							cout << (*n)->node_name() << " -> ";
						cout<<endl;
					}

				break;
			case 3:
				break;
			case 4:
				break;
			case 5:
				break;
			default:
				cout<<"Invalide Choice, please try again."<<endl;
		}

	}

	cout<<"========================================================"<<endl;

	cout<<"Router 1 policy:"<<endl;
	R1.print_info();
	cout<<endl<<endl;

	cout<<"========================================================"<<endl;

	cout<<"Firewall SG-Web policy:"<<endl;
	SGWEB.print_info();
	cout<<"========================================================"<<endl;

	cout<<"Firewall SG-DB policy:"<<endl;
	SGDB.print_info();


	cout<<"========================================================"<<endl;
	// print the first rule in F1
	//cout<<"the 1st rule in F1:"<<endl;
	//N.showFlows(SGWEB.rule(0), 5);

	//cout<<"========================================================"<<endl;
	// reachability test:
	cout<<"reachability test between WEB & DB:"<<endl;
	Query q1;
	q1 = N.checkFlow(WEB,ANY, DB, ANY);
	N.showFlows(q1, 5);


	cout<<"========================================================"<<endl;
	// reachability test:
	cout<<"reachability test between NET & DB:"<<endl;
	q1 = N.checkFlow(NET,ANY, DB, ANY);
	N.showFlows(q1, 5);


	cout<<"========================================================"<<endl;
	 //reachability test:
	cout<<"reachability test between NET & WEB:"<<endl;
	q1 = N.checkFlow(NET,ANY, WEB, ANY);
	N.showFlows(q1, 10);
	
	
	cout<<"========================================================"<<endl;
	//show who can access the web, i.e. dest. port is 80
	bdd dbBDD;
	dbBDD = Restrict(N.globalBDD, DST_IP, "192.168.2.20");
	cout<<"DB traffic: "<<endl;
	N.showFlows(dbBDD, 10);


	cout<<"========================================================"<<endl;
	//show who can access the web, i.e. dest. port is 80
	bdd httpBDD;
	httpBDD = Restrict(N.globalBDD, DST_IP, "192.168.1.20");
	httpBDD = Restrict(httpBDD, DST_PORT, 80);

	cout<<"Web request traffic: "<<endl;
	N.showFlows(httpBDD, 10);

	cout<<"========================================================"<<endl;
	//show who can access the web, i.e. dest. port is 80
	bdd rdpBDD;
	rdpBDD = Restrict(N.globalBDD, DST_IP, "192.168.1.20");
	rdpBDD = Restrict(rdpBDD, DST_PORT, 3306);
	cout<<"Webserver RDP traffic: "<<endl;
	N.showFlows(rdpBDD, 10);

	cout<<"========================================================"<<endl;
	//show who can access the web, i.e. dest. port is 80
	bdd egBDD;
	egBDD = Restrict(N.globalBDD, DST_IP, "151.0.0.30");
	cout<<"Egress traffic: "<<endl;
	N.showFlows(egBDD, 10);
/*
	cout<<"========================================================"<<endl;
	// get list of firewalls between D1 and D2
	vector<firewall_node*> fVec;
	N.getPathObjects(WEB, DB, fVec, FIREWALL);
	cout<<"# of objects = "<<fVec.size()<<endl;
	cout<<"FW1 policy :"<<endl;
	N.showFlows(fVec[0]->policy(), 10);
	fVec[0]->print_info();
	
	
	cout<<"========================================================"<<endl;
	//check shadowing / spuriousness between F1 and F2
	if( (!F1.policy() & (F2.policy())) != bddfalse )
		cout<<"shadowing"<<endl;

	if( (F1.policy() & !(F2.policy())) != bddfalse )
		cout<<"spuriousness"<<endl;



	cout<<"========================================================"<<endl;
	// hidden tunnel between D1 and D2 using D3
	bdd temp13, temp14, temp34;
	
	cout<<"Hidden tunnels analysis:"<<endl;
	temp13= Restrict(N.globalBDD, SRC_IP, "140.192.34.0");
	temp13= Restrict(temp13, DST_IP, "140.192.40.0");

	temp14= Restrict(N.globalBDD, SRC_IP, "140.192.34.0");
	temp14= Restrict(temp14, DST_IP, "140.192.45.0");

	temp34= Restrict(N.globalBDD, SRC_IP, "140.192.40.0");
	temp34= Restrict(temp34, DST_IP, "140.192.45.0");

	if(temp14 == FALSE && temp13 != FALSE && temp34 != FALSE)
		cout<<"Hidden tunnel between D1 and D4 through D3"<<endl;
	*/

	cout<<"========================================================"<<endl;
	cout << "Done" << endl;
	cout<<"num nodes = "<<num_nodes<<endl;
	cout<<"BDD size = "<<bdd_nodecount(N.globalBDD)<<endl;

}