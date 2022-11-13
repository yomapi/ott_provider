# API Documentation

### /audio/

#### POST
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [CreateAudioReqSchema](#CreateAudioReqSchema) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [Audio](#Audio) |

### /audio/{audio_id}

#### POST
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| audio_id | path |  | Yes | string |
| data | body |  | Yes | [UpdateAudioReqSchema](#UpdateAudioReqSchema) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [Audio](#Audio) |

#### DELETE
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| audio_id | path |  | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [IsSuccessResSchema](#IsSuccessResSchema) |

### /audio/{audio_id}/mp3_file

#### GET
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| audio_id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /login/

#### POST
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [UserLoginReqSchema](#UserLoginReqSchema) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [UserLoginResSchema](#UserLoginResSchema) |

### /project/

#### POST
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [CreateProjectReqSchema](#CreateProjectReqSchema) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [Project](#Project) |

### /project/{project_id}

#### DELETE
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| project_id | path |  | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [IsSuccessResSchema](#IsSuccessResSchema) |

### /project/{project_id}/page/{page}

#### GET
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| page | path |  | Yes | string |
| project_id | path |  | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [GetPageResponseSchema](#GetPageResponseSchema) |

### /signup/

#### POST
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | [UserSignUpReqSchema](#UserSignUpReqSchema) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [User](#User) |

### Models


#### CreateAudioReqSchema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| project_id | integer |  | Yes |
| index | integer |  | Yes |
| text | string |  | Yes |
| speed | integer |  | Yes |

#### Audio

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| created_at | dateTime |  | No |
| updated_at | dateTime |  | No |
| index | integer |  | No |
| text | string |  | Yes |
| speed | integer |  | No |
| path | string |  | No |
| is_audio_required | boolean |  | No |
| project | integer |  | Yes |
| user | integer |  | Yes |

#### UpdateAudioReqSchema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| text | string |  | Yes |
| speed | integer |  | Yes |

#### IsSuccessResSchema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| is_success | boolean |  | Yes |

#### UserLoginReqSchema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| email | string |  | Yes |
| password | string |  | Yes |

#### UserLoginResSchema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| access | string |  | Yes |

#### CreateProjectReqSchema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| title | string |  | Yes |
| sentences | string |  | Yes |

#### Project

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| created_at | dateTime |  | No |
| updated_at | dateTime |  | No |
| project_title | string |  | No |
| user | integer |  | Yes |

#### GetPageResponseSchema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| cnt | integer |  | Yes |
| page | [ [Audio](#Audio) ] |  | Yes |

#### UserSignUpReqSchema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| name | string |  | Yes |
| email | string |  | Yes |
| password | string |  | Yes |

#### User

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| created_at | dateTime |  | No |
| updated_at | dateTime |  | No |
| name | string |  | No |
| email | string |  | No |
| password | string |  | No |
