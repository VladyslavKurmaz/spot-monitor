
export class Camera {
  id: number = 0;
  health: boolean = false; 
  cameraIPAddress: string = "";
  username: string = "";
  password: string = "";
  streamDestination: string= "";
  streamUrl: string = "";
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
