<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" @click="toggleAddFileModal">Dokument hinzufügen</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Index</th>
              <th scope="col">Titel</th>
              <th scope="col">Dokumententyp</th>
              <th scope="col">Uploaddatum</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(file, index) in files" :key="index">
              <td>{{ file.index }}</td>
              <td>{{ file.title }}</td>
              <td>{{ file.type }}</td>
              <td>{{ file.date }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Aktualisieren</button>
                  <button type="button" class="btn btn-danger btn-sm">Löschen</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

     <!-- Pop-up um neue Datei hinzuzufügen -->

    <div ref="addFileModal" class="modal fade" :class="{ show: activeAddFileModal, 'd-block': activeAddFileModal }"
      tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Ein neues Dokument hinzufügen.</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="toggleAddFileModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addFile" class="form-label">Title:</label>
                <input type="file" class="form-control" id="addFile" @change="handleFile">
              </div>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-primary btn-sm" @click="handleAddSubmit">
                  Submit
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAddFileModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      activeAddFileModal: false,
      files: [],
    };
  },
  methods: {
    addFile(payload){
      const path = 'http://localhost:5000/files';
      axios.post(path, payload)
        .then(()=>{
          this.getFiles();
        })
        .catch((error) => {
          console.log(error);
          this.getFiles();
        })
    },
    getFiles() {
      const path = 'http://localhost:5000/files';
      axios.get(path)
        .then((res) => {
          this.files = res.data.files;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleAddFileSubmit(){
      this.toggleAddFileModal();
      const payload = {};
      this.addFile(payload);
    },
    toggleAddFileModal(){
      const body = document.querySelector('body');
      this.activeAddFileModal = !this.activeAddFileModal;
      if(this.activeAddFileModal){
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    }
  },
  created() {
    this.getFiles();
  },
};
</script>
