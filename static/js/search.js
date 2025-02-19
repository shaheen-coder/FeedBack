class FB {
    static update_staff_search(data, mode,is_analysis,btn_name) {
        const mainContainer = document.getElementById('dataContainer');
        if (!mainContainer) { console.error('DataContainer not found!'); return; }
        mainContainer.innerHTML = '';
        if (data.datas && data.datas.length > 0) {
            data.datas.forEach(staff => {
                const userDiv = document.createElement('div');
                userDiv.className = 'user';
                if (mode == 'staff') {
                    let url = (!is_analysis) ? `${currentDomain}/prinicipal/report/${mode}/${staff.id}/${staff.dept}/` : `${currentDomain}/analysis/staff/${staff.id}/${staff.dept}/`;
                    (!is_analysis) ? console.log('report') : console.log('analysis');
                    userDiv.innerHTML = `
                    <div class="stafs">
                        <img src="${staff.profile_pic}" alt="User Image">
                    </div>
                    <div>
                        <p>${staff.dept}</p>
                    </div>
                    <div>
                        <p>${staff.name} </p>
                    </div>
                    <a href="${url}" class="data_but">${btn_name}</a>
                `;
                    dataContainer.appendChild(userDiv);
                } else if (mode == 'staffsub') {
                    let url = (!is_analysis) ? `${currentDomain}/prinicipal/report/${mode}/${staff.id}/${staff.dept}/` : `${currentDomain}/analysis/staffsub/${staff.staff.id}/${staff.subject.code}/`;
                    userDiv.innerHTML = `
                    <div class="stafs">
                        <img src="${staff.staff.profile_pic}" alt="User Image">
                    </div>
                    <div>
                        <p>${staff.staff.name} : ${staff.section} </p>
                    </div>
                    <div>
                        <p>${staff.subject.name} </p>
                    </div>
                    <a href="${url}" class="data_but">${btn_name}</a>
                `;
                    dataContainer.appendChild(userDiv);
                }
            });
        } else {
            console.error('API retured 0 data ');
        }
    }
    static update_student_search(data,mode){
        if (data.student && data.student.length > 0) {
            data.student.forEach(student => {
                if(mode == 'stu'){
                    const userDiv = document.createElement('div');
                    userDiv.className = 'user'; 
                    let url = `${currentDomain}/prinicipal/report/${mode}/${student.id}/${student.dept}/`;
                    userDiv.innerHTML = `
                        <div class="stafs">
                            <img src="" alt="User Image">
                        </div>
                        <div>
                            <p>${student.name}</p>
                        </div>
                        <div>
                            <p>${student.dept} </p>
                        </div>
                        <a href="${url}" class="data_but">Report</a>
                    `;
                    dataContainer.appendChild(userDiv);
                }else{
                    const userDiv = document.createElement('div');
                    userDiv.className = 'user'; 
                    let url = `${currentDomain}/cadmin/comment/${student.id}/`;
                    userDiv.innerHTML = `
                        <div class="stafs">
                            <img src="" alt="User Image">
                        </div>
                        <div>
                            <p>${student.name}</p>
                        </div>
                        <div>
                            <p>${student.dept} </p>
                        </div>
                        <a href="${url}" class="data_but">Report</a>
                    `;
                    dataContainer.appendChild(userDiv);
                }
            });
        } else if(data.student.length == 1) {
            const userDiv = document.createElement('div');
                userDiv.className = 'user';
                let url = `${currentDomain}/prinicipal/report/${mode}/${data.student.id}/${data.student.dept}/`;
                userDiv.innerHTML = `
                    <div class="stafs">
                        <img src="" alt="User Image">
                    </div>
                    <div>
                        <p>${data.student.name}</p>
                    </div>
                    <div>
                        <p>${data.student.dept} </p>
                    </div>
                    <a href="${url}" class="data_but">Report</a>
            `;
            dataContainer.appendChild(userDiv);
        }else{
            console.error('API has no data');
        }
    }

    static update_subject(data){
        const container = document.getElementById('course_list');
        console.log(`data : ${JSON.stringify(data)} and len : ${data.length}`);
        if(data && data.data.length > 1){
            data.forEach((item) =>{
                const btn = document.createElement('a');
                btn.className = 'btn btn-outline w-full hover:bg-blue-700 hover:border-blue hover:text-white';
                btn.href = `/mcfeed/${student_id}/${mcourse}/${feed_count}/${item.subject.code}/`;
                btn.textContent = `${item.subject.name} - ${item.subject.code}`;
                container.appendChild(btn);
            })
        }else if (data.data.length == 1 ){
            let item = data.data[0];
            const btn = document.createElement('a');
            btn.className = 'btn btn-outline w-full hover:bg-blue-700 hover:border-blue hover:text-white';
            btn.href = `/mcfeed/${student_id}/${mcourse}/${feed_count}/${item.subject.code}/`;
            btn.textContent = `${item.subject.name} - ${item.subject.code}`;
            container.appendChild(btn);
        }else{
            const error = document.createElement('h1');
            error.className = 'text-3xl font-bold tracking-tight text-red-500 text-center sm:text-4xl';
            error.textContent = 'courses not found';
            container.appendChild(error);
        }
    }
};