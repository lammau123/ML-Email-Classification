import { useState } from 'react';
import axios from 'axios';

function EmailForm() {
    const [form, setForm] = useState({
        Subject: '',
        Body: ''
      });

    const [result, setResult] = useState('');

    async function handleSubmit(e) {
        e.preventDefault();
        try {
            // Make a POST request to the API endpoint
            const response = await axios.post('http://127.0.0.1:5000/api/predict', form);
      
            // Handle successful response
            console.log('Response:', response.data);
            setResult(response.data.type)
          } catch (error) {
            // Handle error
            console.error('Error:', error);
          }
    }

    return (
        <form>
            <div className="card">
                <div className="card-body">
                    <h5 className="card-title"></h5>
                    <div className="row mb-3">
                        <label className="col-sm-2 col-form-label">Subject</label>
                        <div className="col-sm-10">
                        <input type="text" className="form-control" id="inputEmail3" 
                            value={form.Subject}
                            onChange={e => {
                                setForm({
                                  ...form,
                                  Subject: e.target.value
                                });
                              }}/>
                        </div>
                    </div>
                    <div className="row mb-3">
                        <label className="col-sm-2 col-form-label">Body</label>
                        <div className="col-sm-10">
                        <textarea className="form-control" id="exampleFormControlTextarea1"
                            rows={10}
                            cols={50}
                            value={form.Body}
                            onChange={e => {
                                setForm({
                                ...form,
                                Body: e.target.value
                                });
                            }}>
                        </textarea>
                        </div>
                    </div>
                    <div className="row mb-3">
                        <label className="col-sm-2 col-form-label">Type</label>
                        <div className="col-sm-10 " style={{ textAlign: 'left' }}>
                            <b>{result}</b>
                        </div>
                    </div>
                    <button type="submit" className="btn btn-primary" onClick={(e) => handleSubmit(e)}>Submit</button>
                </div>
            </div>
        </form>
    );
}

export default EmailForm