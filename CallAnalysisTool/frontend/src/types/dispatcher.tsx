export interface Dispatcher {
  id: string;
  name: string;
  files: {
    transcriptFiles: string[]; // Transcripted Json Files
    audioFiles: string[]; // Audio Files to be Used when listening to the call
  };
  grades?: {
    [filename: string]: string | number; // Grade for each transcript file
  };
}
