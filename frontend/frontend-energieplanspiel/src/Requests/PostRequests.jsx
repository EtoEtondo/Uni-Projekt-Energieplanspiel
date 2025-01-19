export const addInstitution = async (name) => {
  return fetch("http://localhost:8000/institution/", {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
    body: JSON.stringify({
      name: name,
    }),
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: 0, message: data["Success"] };
    } else {
      return { status: 1, message: data["Error"] };
    }
  });
};

export const addInstructor = async (newEntry, id) => {
  return fetch("http://localhost:8000/instructor/?institution=" + id, {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
    body: JSON.stringify({
      display_name: newEntry.name,
      password: newEntry.password,
      institution: id,
    }),
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: 0, message: data["Success"] };
    } else {
      return { status: 1, message: data["Error"] };
    }
  });
};

export const addSchedule = async (timeslot, id) => {
  return fetch("http://localhost:8000/schedule/?username=" + id, {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
    body: JSON.stringify({
      timeslot: timeslot,
      username: id,
    }),
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: 0, message: data["Success"] };
    } else {
      return { status: 1, message: data["Error"] };
    }
  });
};

export const addGroup = async (newEntry, id) => {
  return fetch("http://localhost:8000/group/?schedule=" + id, {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
    body: JSON.stringify({
      display_name: newEntry.name,
      password: newEntry.password,
      schedule: id,
    }),
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: 0, message: data["Success"] };
    } else {
      return { status: 1, message: data["Error"] };
    }
  });
};

export const addConfig = async (data) => {
  return fetch("http://localhost:8000/input/", {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
    body: data,
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: 0, message: data["Success"] };
    } else {
      return { status: -1};
    }
  });
};

export const submitResults = async (data) => {
  return fetch("http://localhost:8000/input/", {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
    body: JSON.stringify(data),
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: 0, message: data["Success"] };
    } else {
      return { status: 1, message: data["Error"] };
    }
  });
};

export const startCalc = async (schedule) => {
  return fetch("http://localhost:8000/calculate/", {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
    body: JSON.stringify({
      schedule: schedule,
    }),
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: 0, message: data["Success"] };
    } else {
      return { status: 1, message: data["Error"] };
    }
  });
};
