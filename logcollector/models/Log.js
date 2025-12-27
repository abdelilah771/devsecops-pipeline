
const mongoose = require('mongoose');

const LogSchema = new mongoose.Schema({
  log_data: {
    type: mongoose.Schema.Types.Mixed,
    required: true,
  },
  repo_name: {
    type: String,
    required: true,
  },
  author: {
    type: String,
    required: true,
  },
  pipeline_name: {
    type: String,
    required: true,
  },
  run_id: {
    type: String,
    required: true,
  },
  timestamp_original: {
    type: Date,
  },
  timestamp_received: {
    type: Date,
    default: Date.now,
  },
  source: {
    type: String,
    required: true,
  },
});

module.exports = mongoose.model('Log', LogSchema);
