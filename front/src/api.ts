import Axios from 'axios'


const api = Axios.create({
  // axiosインスタンスの作成
  baseURL: location.protocol + '//' + location.hostname + '/api/contests',
  headers: {
    'Content-Type': 'application/json'
  },
  responseType: 'json'
})

export default api;
