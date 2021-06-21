import React from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';

import Container from 'react-bootstrap/Container';

import * as Service from '../services/communication';


class Programs extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            programsData: '',
        }

        this.fetchPrograms(); // to fetch the programs' data
    }


    fetchPrograms() {
        const promise = Service.fetchPrograms();
        promise.then((data) => {
            if (data !== undefined) {
                if (data["data"] != null) {
                    this.setState({programsData: data["data"]});
                }
                else {
                    alert(data["msg"]);
                }
            }
            else {
                alert("Connection error with the server, response is undefined");
            }
        });
    }

    updatePrograms() {
        const promise = Service.updatePrograms();
        promise.then((data) => {
            if (data !== undefined) {
                if (data["data"] != null) {
                    this.setState({programsData: data["data"]});
                }
                else {
                    alert(data["msg"]);
                }
            }
            else {
                alert("Connection error with the server, response is undefined");
            }
        });
    }


    /**
     * Function to display the table header - Disease Funds, Treatments Covered, status, Maximum Award Level
     */
    renderTableHeader() {
        return (            
            <tr>
                <th>#</th>
                <th>Disease Funds</th>
                <th>Status</th>
                <th>Maximum Award Level</th>
                <th>Treatments Covered</th>
            </tr>
        );
    }


    renderTableData(){
        var tableIdx = 0;
        return this.state.programsData.map((program, index) => {
            console.log(program);
            const {disease_funds, treatments_covered, status, max_award_level} = program;
            tableIdx +=1;
            
            return (
                <tr>
                    <td>{tableIdx}</td>
                    <td>{disease_funds}</td>
                    <td>{status}</td>
                    <td>{max_award_level}</td>
                    <td>{treatments_covered}</td>
                </tr>
            );
        });
    }



    render() {

        return (
            <div style={{ marginRight: "1%", marginLeft: "1%", marginBottom: "3%" }}>
                <div style={{ marginTop: "1%", display: "flex", justifyContent: "center", alignItems: "center" }}>
                    <h2>Welcome to Assistance Programs Watcher</h2>
                </div>
                <br />
                
                {this.state.programsData ?
                <div>
                    <div>
                    <Container fluid>
                    <Table class="table" striped bordered hover variant="outline-info">
                        <thead>
                            {this.state.programsData ? this.renderTableHeader() : null}
                        </thead>
                        <tbody>
                            {this.state.programsData ? this.renderTableData() : null}
                        </tbody>
                    </Table>
                    </Container>
                    </div>

                    <div>      
                    <Button block variant='outline-info' onClick={() => this.updatePrograms()}>
                        Refresh
                    </Button>
                    </div>
                </div>
                :

                <div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
                    Please wait, the table is loading... 
                </div>
                }
                
            </div>
        );
    }
}


export default Programs;