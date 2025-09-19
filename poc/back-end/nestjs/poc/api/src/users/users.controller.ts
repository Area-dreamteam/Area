import { Controller, Get, Param, Patch, Body, UseGuards, Request } from '@nestjs/common';
import { UsersService } from './users.service';
import { UpdateUserDto } from './dto/update_user.dto';
import { ApiTags, ApiOperation, ApiOkResponse } from '@nestjs/swagger';
import { Roles } from '../common/decorators/roles.decorator';
import { UserId } from '../common/decorators/user.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { JwtAuthGuard } from '../common/guards/jwtAuth.guard';
import { Role } from '../common/enum/role.enum';
import { UserDto } from './dto/user.dto';

@ApiTags('users')
@Controller('users')
@UseGuards(JwtAuthGuard, RolesGuard)
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get('me')
  @ApiOperation({ summary: 'get login user information' })
  @ApiOkResponse({
    description: 'Returns the current user',
    type: UserDto,
  })
  async getCurrentUser(@UserId() userId: number) {
    return this.usersService.findById(userId);
  }

  @Get(':id')
  @Roles(Role.Admin)
  @ApiOperation({ summary: 'get a user by ID (admin only)' })
  @ApiOkResponse({
    description: 'Returns a user by ID',
    type: UserDto,
  })
  async findById(@Param('id') id: number) {
    return this.usersService.findById(Number(id));
  }

  @Patch(':id')
  @Roles(Role.Admin)
  @ApiOperation({ summary: 'update a user by ID (admin only)' })
  @ApiOkResponse({
    description: 'Updated user object',
    type: UserDto,
  })
  async update(@Param('id') id: number, @Body() dto: UpdateUserDto) {
    return this.usersService.update(Number(id), dto);
  }
}
