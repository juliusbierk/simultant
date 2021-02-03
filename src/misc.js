import { v4 as uuidv4 } from "uuid";

export default {
  parameter_uuid: function() {
    return "par_" + uuidv4();
  },
  model_uuid: function() {
    return "model_" + uuidv4();
  },
  data_uuid: function() {
    return "data_" + uuidv4();
  }
};
