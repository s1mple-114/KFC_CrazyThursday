import axios from 'axios'

const request = axios.create({
  baseURL: 'http://192.168.43.105:8000/api/',
  timeout: 50000
})

export default request