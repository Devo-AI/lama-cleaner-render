<script lang="ts">
  let targetPlatform = 'instagram';
  let file: File | null = null;
  let status = '';
  let outputUrl = '';
  let error = '';

  async function submitForm() {
    if (!file) {
      error = 'Please upload a video file.';
      return;
    }

    const formData = new FormData();
    formData.append('target_platform', targetPlatform);
    formData.append('file', file);

    status = 'Processing...';
    error = '';
    outputUrl = '';

    try {
      const res = await fetch('http://localhost:8000/repurpose', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        throw new Error('Video processing failed.');
      }

      const blob = await res.blob();
      outputUrl = URL.createObjectURL(blob);
      status = 'Done!';
    } catch (err) {
      error = err.message;
      status = '';
    }
  }
</script>

<style>
  main {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    font-family: sans-serif;
    background: #f9f9f9;
    border-radius: 10px;
  }

  h1 {
    text-align: center;
  }

  label {
    font-weight: bold;
    margin-top: 1rem;
  }

  select, input[type="file"] {
    display: block;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
  }

  button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #0d6efd;
    color: white;
    border: none;
    border-radius: 5px;
  }

  .status {
    margin-top: 1rem;
    font-style: italic;
  }

  video {
    margin-top: 1rem;
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 8px;
  }

  .error {
    color: red;
    margin-top: 1rem;
  }
</style>

<main>
  <h1>Repurpose Your TikTok Video</h1>

  <label for="platform">Choose Target Platform:</label>
  <select bind:value={targetPlatform} id="platform">
    <option value="instagram">Instagram Reels</option>
    <option value="youtube">YouTube Shorts</option>
  </select>

  <label for="file">Upload TikTok Video:</label>
  <input type="file" id="file" accept="video/*" on:change={(e) => file = e.target.files[0]} />

  <button on:click={submitForm}>Upload & Convert</button>

  {#if status}
    <div class="status">{status}</div>
  {/if}

  {#if error}
    <div class="error">{error}</div>
  {/if}

  {#if outputUrl}
    <h3>Converted Video:</h3>
    <video controls src={outputUrl}></video>
  {/if}
</main>
