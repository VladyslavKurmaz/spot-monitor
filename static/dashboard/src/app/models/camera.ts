
export class Camera {
  id: number = 0;
  health: boolean = false; 
  ip: string = "";
  user: string = "";
  password: string = "";
  endpoint: string= "";
  streamUrl: string = "";
  videoSource: string = "";
}

export class Response {
  status: Boolean = false;
  message: String = ""; 
}

export class CameraResponse extends Response {
  data: Camera = null; 
}

export class CamerasResponse extends Response {
  data: Camera[] = null; 
}
