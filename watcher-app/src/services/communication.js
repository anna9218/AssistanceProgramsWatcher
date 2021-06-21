import axios from "axios";
var ip = "localhost";
var port = "5000";


export async function fetchPrograms(){
    return axios.get('http://' + ip + ':' + port + '/fetch_programs')
    .then((response) => (response.data), (error) => {console.log(error)});
}

export async function updatePrograms(){
    return axios.get('http://' + ip + ':' + port + '/update_programs')
    .then((response) => (response.data), (error) => {console.log(error)});
}