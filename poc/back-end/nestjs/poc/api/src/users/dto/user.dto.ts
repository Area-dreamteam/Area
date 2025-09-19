import { ApiProperty } from '@nestjs/swagger';
import { Role } from '../../common/enum/role.enum';

export class UserDto {
  @ApiProperty({ example: 1 })
  id: number;

  @ApiProperty({ example: 'john_doe' })
  username: string;

  @ApiProperty({ example: 'john@example.com' })
  email: string;

  @ApiProperty({ example: Role.User, enum: Role })
  role: Role;

  @ApiProperty({ example: '2025-09-19T12:34:56.000Z' })
  createdAt: Date;

  @ApiProperty({ example: '2025-09-19T12:34:56.000Z' })
  updatedAt: Date;
}
