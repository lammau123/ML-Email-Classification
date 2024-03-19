
import { useState } from 'react';

function EmailForm() {
    const [form, setForm] = useState({
        subject: '',
        body: ''
      });

    function handleSubmit(e) {
        e.preventDefault();
    }

    return (
        <form>
            <div className="card">
                <div className="card-body">
                    <h5 className="card-title">Email Form</h5>
                    <div className="row mb-3">
                        <label className="col-sm-2 col-form-label">Subject</label>
                        <div className="col-sm-10">
                        <input type="text" className="form-control" id="inputEmail3" 
                            value={form.subject}
                            onChange={e => {
                                setForm({
                                  ...form,
                                  subject: e.target.value
                                });
                              }}/>
                        </div>
                    </div>
                    <div className="row mb-3">
                        <label className="col-sm-2 col-form-label">Body</label>
                        <div className="col-sm-10">
                        <textarea className="form-control" id="exampleFormControlTextarea1"
                            onChange={e => {
                                setForm({
                                ...form,
                                body: e.target.value
                                });
                            }}>
                            {form.body}
                        </textarea>
                        </div>
                    </div>
                    <button type="submit" className="btn btn-primary" onClick={(e) => handleSubmit(e)}>Submit</button>
                </div>
            </div>
        </form>
    );
}

export default EmailForm