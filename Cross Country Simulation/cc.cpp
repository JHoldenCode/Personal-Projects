#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>
using namespace std;

int simulateRace(int& perfectWins, int& winsWhen1stPlace, int& winsWhenTop2Place, int& numRacesWithTop2Same,
	int& numRacesWithTop3Same, int& winsWhenTop3Place, int& ties);

int main() {
	srand(static_cast<unsigned>(time(0)));
	int numRaces, zWins = 0, oWins = 0;
	int perfectWins = 0, ties = 0;

	// statistics section
	int numWinsWhen1stPlace = 0, numWinsWhenTop2Place = 0, numWinsWhenTop3Place = 0;
	int numRacesWithTop2Same = 0, numRacesWithTop3Same = 0;

	cout << "How many races would you like to simulate? ";
	cin >> numRaces;
	
	for (int i = 0; i < numRaces; i++) {
		if (simulateRace(perfectWins, numWinsWhen1stPlace, numWinsWhenTop2Place, numRacesWithTop2Same, 
			numRacesWithTop3Same, numWinsWhenTop3Place, ties)) oWins++;
		else zWins++;
	}

	cout << "Team 0 had: " << zWins << " wins." << endl;
	cout << "Team 1 had: " << oWins << " wins." << endl;
	cout << "There were " << ties << " ties." << endl;
	cout << "There were " << perfectWins << " perfect wins!" << endl;
	cout << "When a team had an athlete finish 1st place, their chance of winning was: "
		<< static_cast<double>(numWinsWhen1stPlace) / numRaces * 100 << "%" << endl;
	cout << "When a team had athletes finish int the top 2 places, their chance of winning was: "
		<< static_cast<double>(numWinsWhenTop2Place) / numRacesWithTop2Same * 100 << "%" << endl;
	cout << "When a team had athletes finish int the top 3 places, their chance of winning was: "
		<< static_cast<double>(numWinsWhenTop3Place) / numRacesWithTop3Same * 100 << "%" << endl;

	return 0;
}

int simulateRace(int &perfectWins, int& winsWhen1stPlace, int& winsWhenTop2Place, int& numRacesWithTop2Same,
	int& numRacesWithTop3Same, int& winsWhenTop3Place, int& ties) {
	vector<int> v;
	vector<int> winningPlaces;
	int team0Score = 0, team1Score = 0;
	int team0Finished = 0, team1Finished = 0;
	int team06Place, team16Place;

	// simulate places
	for (int i = 0; i < 14; i++) {
		if (team0Finished >= 7) {
			v.push_back(1);
			if (team1Finished < 5) team1Score += i + 1;
			if (team1Finished == 5) team16Place = i;
			team1Finished++;
		}
		else if (team1Finished >= 7) {
			v.push_back(0);
			if (team0Finished < 5) team0Score += i + 1;
			if (team0Finished == 5) team06Place = i;
			team0Finished++;
		}
		else {
			int team = rand() % 2;
			if (team == 0) {
				if (team0Finished < 5) team0Score += i + 1;
				if (team0Finished == 5) team06Place = i;
				team0Finished++;
			}
			else {
				if (team1Finished < 5) team1Score += i + 1;
				if (team1Finished == 5) team16Place = i;
				team1Finished++;
			}
			v.push_back(team);
		}
		//cout << i + 1 << " place: " << v[v.size() - 1] << endl;
	}
	
	// calculate winner
	int winner;
	if (team0Score < team1Score) winner = 0;
	else if (team1Score < team0Score) winner = 1;
	else {
		//if (v[0] == v[1]) exit(1);
		if (team06Place < team16Place) winner = 0;
		else if (team16Place < team06Place) winner = 1;
		else exit(1);
	}
	//cout << "Team 0 Score: " << team0Score << ", Team 1 Score: " << team1Score << endl;
	//cout << "Team " << winner << " wins!" << endl;

	if (team0Score == 50 || team1Score == 50) perfectWins++;

	// calculate statistics
	if (v[0] == winner) winsWhen1stPlace++;

	if (v[0] == v[1]) {
		if (v[0] == winner) winsWhenTop2Place++;
		numRacesWithTop2Same++;
	}

	if (v[0] == v[1] && v[1] == v[2]) {
		if (v[0] == winner) winsWhenTop3Place++;
		numRacesWithTop3Same++;
	}

	return winner;
}
